"""
Flask API Backend for ClauseAI React Frontend
Handles file uploads and connects to the multi-agent analyzer
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import sys
import tempfile
from datetime import datetime

# Fix Windows console UTF-8 encoding for emoji support
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
from dotenv import load_dotenv
from enum import Enum
import io

# Import existing modules
from multi_agent_analyzer import MultiAgentContractAnalyzer
from document_parser import DocumentParser
from report_generator import ReportGenerator, ReportOptions, ReportTone, ReportFormat

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend


def make_json_serializable(obj):
    """Convert non-serializable objects to JSON-compatible format"""
    if isinstance(obj, Enum):
        return obj.value
    elif isinstance(obj, dict):
        return {k: make_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_json_serializable(item) for item in obj]
    elif hasattr(obj, '__dict__'):
        # Convert dataclass or object to dict
        result = {}
        for key, value in obj.__dict__.items():
            result[key] = make_json_serializable(value)
        return result
    return obj


@app.route('/analyze', methods=['POST'])
def analyze_contract():
    """
    Analyze uploaded contract document
    Supports multilingual results
    
    Form params:
        file: Contract file (PDF/DOCX)
        language: Optional target language (en, ta, hi, te, ml) - Default: en
    """
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Get language parameter (default to English)
        language = request.form.get('language', 'en').lower()
        
        # Validate language
        supported_languages = ['en', 'ta', 'hi', 'te', 'ml']
        if language not in supported_languages:
            return jsonify({
                'error': f'Unsupported language: {language}. Supported: {", ".join(supported_languages)}'
            }), 400
        
        # Save file temporarily
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, file.filename)
        file.save(temp_path)
        
        try:
            # Initialize analyzer
            print(f"[FILE] Parsing document: {file.filename}")
            print(f"[LANG] Target language: {language.upper()}")
            print("[INIT] Initializing multi-agent analyzer...")
            analyzer = MultiAgentContractAnalyzer()
            
            # Analyze contract with language parameter
            print("[ANALYZE] Starting contract analysis...")
            results = analyzer.analyze_contract(temp_path, language=language)
            
            # Convert to JSON-serializable format
            results = make_json_serializable(results)
            
            # Load contract context into chatbot for Q&A
            try:
                contract_id = results.get('contract_id')
                if contract_id:
                    chatbot.load_contract_context(contract_id, results)
                    print("[CHAT] Chatbot context loaded - ready for Q&A!")
            except Exception as chat_error:
                print(f"[WARNING] Chatbot context load failed (non-critical): {str(chat_error)}")
            
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            print("[OK] Analysis complete!")
            return jsonify(results), 200
            
        except Exception as e:
            # Clean up temp file on error
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise e
        
    except Exception as e:
        print(f"[ERROR] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': f'Error analyzing contract: {str(e)}'
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'ClauseAI Backend API',
        'version': '1.0.0'
    }), 200


@app.route('/test-translation', methods=['POST'])
def test_translation():
    """
    Test translation endpoint for debugging
    Request body: {"text": "...", "language": "ta|hi|te|ml"}
    """
    try:
        data = request.get_json()
        text = data.get('text', '')
        language = data.get('language', 'en')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        from multilingual_engine import MultilingualEngine
        engine = MultilingualEngine()
        
        translated = engine.translate_text(text, language)
        
        return jsonify({
            'original': text,
            'translated': translated,
            'language': language
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Initialize chatbot globally
from contract_chatbot import ContractChatbot
chatbot = ContractChatbot()


@app.route('/chat', methods=['POST'])
def chat_with_contract():
    """
    Chat endpoint for interactive Q&A with contract
    
    Request body:
    {
        "contract_id": "abc123",
        "question": "What is my payment obligation?",
        "language": "en|ta|hi|te|ml"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        contract_id = data.get('contract_id')
        question = data.get('question')
        language = data.get('language', 'en')
        
        if not contract_id:
            return jsonify({'error': 'contract_id is required'}), 400
        
        if not question:
            return jsonify({'error': 'question is required'}), 400
        
        # Get answer from chatbot
        result = chatbot.answer_question(contract_id, question, language)
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"[ERROR] Chat error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': f'Error processing chat: {str(e)}'
        }), 500


@app.route('/chat/load-context', methods=['POST'])
def load_chat_context():
    """
    Load contract analysis into chatbot context
    Called automatically after contract analysis
    
    Request body:
    {
        "contract_id": "abc123",
        "analysis_results": {...}
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        contract_id = data.get('contract_id')
        analysis_results = data.get('analysis_results')
        
        if not contract_id or not analysis_results:
            return jsonify({'error': 'contract_id and analysis_results are required'}), 400
        
        # Load context into chatbot
        chatbot.load_contract_context(contract_id, analysis_results)
        
        # Get suggested questions
        suggestions = chatbot.get_suggested_questions(contract_id)
        
        return jsonify({
            'status': 'success',
            'message': 'Context loaded successfully',
            'suggested_questions': suggestions
        }), 200
        
    except Exception as e:
        print(f"[ERROR] Load context error: {str(e)}")
        return jsonify({
            'error': f'Error loading context: {str(e)}'
        }), 500


@app.route('/chat/suggestions/<contract_id>', methods=['GET'])
def get_chat_suggestions(contract_id):
    """Get suggested questions for a contract"""
    try:
        suggestions = chatbot.get_suggested_questions(contract_id)
        return jsonify({
            'suggestions': suggestions
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/generate-report', methods=['POST'])
def generate_report():
    """
    Generate customized report from analysis results
    Milestone 4: Report Generation Module
    
    Request body:
    {
        "analysis_results": {...},
        "tone": "professional|technical|executive|detailed",
        "format": "markdown|json|html|pdf|docx",
        "include_clauses": true,
        "include_risks": true,
        "include_discussions": true,
        "focus_areas": ["compliance", "finance", "legal", "operations"]
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'analysis_results' not in data:
            return jsonify({'error': 'Missing analysis_results in request body'}), 400
        
        # Parse options
        tone_str = data.get('tone', 'professional')
        format_str = data.get('format', 'markdown')
        
        options = ReportOptions(
            tone=ReportTone(tone_str),
            format=ReportFormat(format_str),
            include_clauses=data.get('include_clauses', True),
            include_risks=data.get('include_risks', True),
            include_discussions=data.get('include_discussions', True),
            include_recommendations=data.get('include_recommendations', True),
            focus_areas=data.get('focus_areas', ['compliance', 'finance', 'legal', 'operations'])
        )
        
        # Generate report
        print(f"[REPORT] Generating {tone_str} report in {format_str} format...")
        generator = ReportGenerator(options)
        report_content = generator.generate_report(data['analysis_results'])
        
        print("[OK] Report generated!")
        
        # Return based on format
        if format_str == 'pdf':
            # Return PDF as binary file
            return send_file(
                io.BytesIO(report_content),
                mimetype='application/pdf',
                as_attachment=True,
                download_name=f'contract-report-{datetime.now().strftime("%Y%m%d-%H%M%S")}.pdf'
            )
        elif format_str == 'docx':
            # Return DOCX as binary file
            return send_file(
                io.BytesIO(report_content),
                mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                as_attachment=True,
                download_name=f'contract-report-{datetime.now().strftime("%Y%m%d-%H%M%S")}.docx'
            )
        elif format_str == 'json':
            return jsonify({'report': report_content}), 200
        else:
            return jsonify({
                'report': report_content,
                'format': format_str,
                'tone': tone_str
            }), 200
            
    except Exception as e:
        print(f"[ERROR] Report generation error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': f'Error generating report: {str(e)}'
        }), 500


@app.route('/analyze-and-report', methods=['POST'])
def analyze_and_report():
    """
    Analyze contract and generate report in one call
    Milestone 4: Integrated workflow
    """
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Get report options from form data
        tone = request.form.get('tone', 'professional')
        format_type = request.form.get('format', 'markdown')
        
        # Save file temporarily
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, file.filename)
        file.save(temp_path)
        
        try:
            # Analyze contract
            print(f"[FILE] Analyzing document: {file.filename}")
            analyzer = MultiAgentContractAnalyzer()
            results = analyzer.analyze_contract(temp_path)
            results = make_json_serializable(results)
            
            # Generate report
            print(f"[REPORT] Generating {tone} report...")
            options = ReportOptions(tone=ReportTone(tone), format=ReportFormat(format_type))
            generator = ReportGenerator(options)
            report = generator.generate_report(results)
            
            # Clean up
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            print("[OK] Analysis and report complete!")
            
            return jsonify({
                'analysis': results,
                'report': report,
                'format': format_type
            }), 200
            
        except Exception as e:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise e
        
    except Exception as e:
        print(f"[ERROR] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': f'Error: {str(e)}'
        }), 500


@app.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    """
    Convert text to speech
    
    Request body:
    {
        "text": "Text to convert to speech",
        "language": "en|ta|hi|te|ml" (optional, default: "en")
    }
    
    Returns: Audio file (MP3)
    """
    try:
        import pyttsx3
        import tempfile
        
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Missing text in request body'}), 400
        
        text = data.get('text', '')
        language = data.get('language', 'en')
        
        if not text:
            return jsonify({'error': 'Text cannot be empty'}), 400
        
        print(f"[TTS] Converting text to speech (language: {language})...")
        
        # Initialize text-to-speech engine
        engine = pyttsx3.init()
        
        # Set properties based on language
        voices = engine.getProperty('voices')
        
        # Configure voice based on language
        if language == 'ta':
            # Try to find Tamil voice (may not be available on all systems)
            for voice in voices:
                if 'tamil' in voice.name.lower() or 'ta' in voice.languages:
                    engine.setProperty('voice', voice.id)
                    break
        elif language == 'hi':
            # Try to find Hindi voice
            for voice in voices:
                if 'hindi' in voice.name.lower() or 'hi' in voice.languages:
                    engine.setProperty('voice', voice.id)
                    break
        # Add more language support as needed
        
        # Set speech rate and volume
        engine.setProperty('rate', 150)  # Speed of speech
        engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)
        
        # Create temporary file for audio
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        temp_path = temp_file.name
        temp_file.close()
        
        # Save speech to file
        engine.save_to_file(text, temp_path)
        engine.runAndWait()
        
        print("[OK] Text-to-speech conversion complete!")
        
        # Return audio file
        return send_file(
            temp_path,
            mimetype='audio/mpeg',
            as_attachment=True,
            download_name=f'contract-audio-{datetime.now().strftime("%Y%m%d-%H%M%S")}.mp3'
        )
        
    except Exception as e:
        print(f"[ERROR] Text-to-speech error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': f'Error converting text to speech: {str(e)}'
        }), 500


if __name__ == '__main__':
    print("=" * 60)
    print("🚀 ClauseAI Backend API Starting...")
    print("=" * 60)
    print("📡 Server: http://localhost:8000")
    print("🔗 CORS: Enabled for frontend")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=8000, debug=True)
