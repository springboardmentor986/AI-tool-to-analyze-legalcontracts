"""
Parallel Clause Extraction Module
Week 3-4 Implementation

Extracts contract clauses across multiple domains in parallel:
- Compliance clauses
- Financial clauses
- Legal clauses
- Operational clauses
"""

import re
import sys
from typing import Dict, List

# Fix Windows console UTF-8 encoding for emoji support
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass


@dataclass
class ExtractedClause:
    """Structure for extracted clause data"""
    clause_type: str
    domain: str
    text: str
    location: str  # Page or paragraph reference
    confidence: float


class ParallelClauseExtractor:
    """
    Parallel processing for multi-domain clause extraction
    Uses ThreadPoolExecutor for concurrent extraction
    """
    
    def __init__(self):
        self.clause_patterns = self._initialize_patterns()
        
    def _initialize_patterns(self) -> Dict[str, Dict[str, List[str]]]:
        """Initialize regex patterns for different clause types across domains"""
        return {
            'compliance': {
                'regulatory': [
                    r'regulatory\s+(?:compliance|requirement|obligation)',
                    r'(?:GDPR|CCPA|HIPAA|SOX)\s+compliance',
                    r'data\s+protection\s+(?:law|regulation)',
                    r'regulatory\s+(?:authority|body|oversight)'
                ],
                'audit': [
                    r'audit\s+(?:right|requirement|obligation)',
                    r'inspection\s+(?:right|requirement)',
                    r'record[s]?\s+(?:keeping|retention|maintenance)',
                    r'compliance\s+(?:audit|review|inspection)'
                ],
                'reporting': [
                    r'reporting\s+(?:obligation|requirement|duty)',
                    r'notification\s+requirement',
                    r'disclosure\s+obligation',
                    r'shall\s+(?:report|notify|disclose)'
                ],
                'data_protection': [
                    r'personal\s+data',
                    r'confidential(?:ity)?\s+(?:obligation|requirement)',
                    r'privacy\s+(?:policy|requirement|obligation)',
                    r'data\s+(?:security|breach|protection)'
                ]
            },
            'finance': {
                'payment_terms': [
                    r'payment\s+(?:term|schedule|due)',
                    r'invoice\s+(?:date|schedule|requirement)',
                    r'(?:net\s+\d+|upon\s+(?:receipt|delivery))',
                    r'shall\s+pay'
                ],
                'pricing': [
                    r'(?:price|fee|cost|charge)[s]?\s+(?:of|for)',
                    r'pricing\s+(?:structure|model|schedule)',
                    r'(?:USD|EUR|GBP|\$|€|£)\s*\d+',
                    r'rate\s+(?:of|per)'
                ],
                'penalties': [
                    r'late\s+(?:payment|fee|penalty)',
                    r'penalty\s+(?:for|of|amount)',
                    r'interest\s+(?:rate|charge)',
                    r'liquidated\s+damages'
                ],
                'expenses': [
                    r'(?:reimburse|reimbursement)\s+(?:of|for)',
                    r'expense[s]?\s+(?:report|reimbursement)',
                    r'out-of-pocket',
                    r'travel\s+expenses?'
                ]
            },
            'legal': {
                'liability': [
                    r'liability\s+(?:for|of|limited|unlimited)',
                    r'limitation\s+of\s+liability',
                    r'indemnif(?:y|ication)',
                    r'hold\s+harmless'
                ],
                'termination': [
                    r'terminat(?:e|ion)\s+(?:of|this|the|agreement)',
                    r'cancel(?:lation|led)',
                    r'(?:early|immediate)\s+termination',
                    r'notice\s+(?:of|to)\s+terminat'
                ],
                'ip_rights': [
                    r'intellectual\s+property',
                    r'(?:copyright|patent|trademark|trade\s+secret)',
                    r'ownership\s+(?:of|rights)',
                    r'proprietary\s+(?:right|information)'
                ],
                'dispute_resolution': [
                    r'dispute\s+resolution',
                    r'arbitration',
                    r'(?:mediation|litigation)',
                    r'governing\s+law'
                ]
            },
            'operations': {
                'deliverables': [
                    r'deliverable[s]?',
                    r'shall\s+(?:deliver|provide|supply)',
                    r'(?:work\s+product|output|result)',
                    r'acceptance\s+(?:criteria|test)'
                ],
                'timelines': [
                    r'deadline[s]?',
                    r'(?:within|by)\s+\d+\s+(?:days?|weeks?|months?)',
                    r'(?:start|end|completion)\s+date',
                    r'milestone[s]?'
                ],
                'sla': [
                    r'service\s+level\s+(?:agreement|objective)',
                    r'(?:SLA|uptime|availability)',
                    r'performance\s+(?:metric|standard|requirement)',
                    r'response\s+time'
                ],
                'warranty': [
                    r'warrant(?:y|ies)',
                    r'guarantee[s]?',
                    r'representation[s]?\s+and\s+warrant',
                    r'warranty\s+period'
                ]
            }
        }
    
    def extract_clauses_parallel(self, contract_text: str, metadata: Dict = None) -> Dict[str, List[ExtractedClause]]:
        """
        Extract clauses from contract text using parallel processing
        
        Args:
            contract_text: Full contract text
            metadata: Optional metadata (page numbers, etc.)
            
        Returns:
            Dictionary of extracted clauses by domain
        """
        results = {
            'compliance': [],
            'finance': [],
            'legal': [],
            'operations': []
        }
        
        # Use ThreadPoolExecutor for parallel extraction
        with ThreadPoolExecutor(max_workers=4) as executor:
            # Submit extraction tasks for each domain
            future_to_domain = {
                executor.submit(self._extract_domain_clauses, domain, contract_text, metadata): domain
                for domain in ['compliance', 'finance', 'legal', 'operations']
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_domain):
                domain = future_to_domain[future]
                try:
                    clauses = future.result()
                    results[domain] = clauses
                    print(f"[OK] {domain.capitalize()} clauses extracted: {len(clauses)} found")
                except Exception as e:
                    print(f"[ERROR] Error extracting {domain} clauses: {str(e)}")
        
        return results
    
    def _extract_domain_clauses(self, domain: str, contract_text: str, metadata: Dict = None) -> List[ExtractedClause]:
        """Extract clauses for a specific domain"""
        clauses = []
        patterns = self.clause_patterns.get(domain, {})
        
        # Split text into paragraphs for better location tracking
        paragraphs = self._split_into_paragraphs(contract_text)
        
        for clause_type, pattern_list in patterns.items():
            for para_idx, paragraph in enumerate(paragraphs):
                for pattern in pattern_list:
                    matches = re.finditer(pattern, paragraph, re.IGNORECASE)
                    for match in matches:
                        # Extract context around the match (100 chars before and after)
                        start = max(0, match.start() - 100)
                        end = min(len(paragraph), match.end() + 100)
                        context = paragraph[start:end]
                        
                        clause = ExtractedClause(
                            clause_type=clause_type,
                            domain=domain,
                            text=context.strip(),
                            location=f"Paragraph {para_idx + 1}",
                            confidence=self._calculate_confidence(match, paragraph)
                        )
                        clauses.append(clause)
                        break  # Only take first match per paragraph per pattern
        
        return clauses
    
    def _split_into_paragraphs(self, text: str) -> List[str]:
        """Split contract text into paragraphs"""
        # Split on double newlines or page markers
        paragraphs = re.split(r'\n\n+|---\s*Page\s+\d+\s*---', text)
        return [p.strip() for p in paragraphs if p.strip()]
    
    def _calculate_confidence(self, match, paragraph: str) -> float:
        """Calculate confidence score for extracted clause"""
        # Simple confidence based on match quality
        confidence = 0.5
        
        # Increase confidence if match is at start of sentence
        if match.start() == 0 or paragraph[match.start()-1] in '.!?\n':
            confidence += 0.2
        
        # Increase confidence if followed by colon or specific keywords
        match_end = match.end()
        if match_end < len(paragraph) - 1:
            next_chars = paragraph[match_end:match_end+10].lower()
            if ':' in next_chars or 'shall' in next_chars or 'must' in next_chars:
                confidence += 0.2
        
        return min(confidence, 1.0)
    
    def get_summary_statistics(self, extracted_clauses: Dict[str, List[ExtractedClause]]) -> Dict:
        """Generate summary statistics for extracted clauses"""
        stats = {
            'total_clauses': 0,
            'by_domain': {},
            'by_clause_type': {},
            'high_confidence_count': 0
        }
        
        for domain, clauses in extracted_clauses.items():
            stats['by_domain'][domain] = len(clauses)
            stats['total_clauses'] += len(clauses)
            
            for clause in clauses:
                clause_type = clause.clause_type
                stats['by_clause_type'][clause_type] = stats['by_clause_type'].get(clause_type, 0) + 1
                
                if clause.confidence >= 0.7:
                    stats['high_confidence_count'] += 1
        
        return stats


if __name__ == "__main__":
    # Test the parallel clause extractor
    print("Parallel Clause Extractor - Week 3")
    print("=" * 60)
    
    sample_text = """
    PAYMENT TERMS: The Client shall pay the Contractor within 30 days of invoice date.
    Late payment penalty of 1.5% per month will apply.
    
    TERMINATION: Either party may terminate this agreement with 30 days written notice.
    
    COMPLIANCE: This agreement shall comply with all applicable GDPR requirements and 
    data protection regulations. Regular compliance audits will be conducted.
    
    DELIVERABLES: The Contractor shall deliver the work product by December 31, 2024.
    Service level agreement requires 99.9% uptime.
    
    LIABILITY: Limitation of liability shall not exceed the total contract value.
    The Contractor shall indemnify the Client against third-party claims.
    """
    
    extractor = ParallelClauseExtractor()
    results = extractor.extract_clauses_parallel(sample_text)
    
    print("\n[DATA] Extraction Results:")
    for domain, clauses in results.items():
        print(f"\n{domain.upper()} ({len(clauses)} clauses):")
        for clause in clauses:
            print(f"  - {clause.clause_type}: {clause.text[:80]}...")
    
    stats = extractor.get_summary_statistics(results)
    print(f"\n📈 Statistics: {stats['total_clauses']} total clauses")
    print(f"High confidence: {stats['high_confidence_count']}")
