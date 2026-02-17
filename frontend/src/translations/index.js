/**
 * Multilingual Translations for ClauseAI
 * Supports: English, Tamil, Hindi, Telugu, Malayalam
 */

const translations = {
  en: {
    // App Title
    appName: 'ClauseAI',
    tagline: 'AI-Powered Legal Contract Analyzer',

    // Navigation
    nav: {
      home: 'Home',
      dashboard: 'Dashboard',
      analyze: 'Analyze Contract',
      reports: 'Reports',
      settings: 'Settings'
    },

    // File Upload
    upload: {
      title: 'Upload Contract',
      dragDrop: 'Drag & drop your contract here',
      or: 'or',
      browse: 'Browse Files',
      supported: 'Supported formats: PDF, DOCX, TXT',
      maxSize: 'Maximum size: 10MB',
      analyzing: 'Analyzing contract...',
      pleaseWait: 'Please wait while our AI agents analyze your contract',
      error: 'Upload failed. Please try again.',
      selectFile: 'Please select a file to upload'
    },

    // Dashboard
    dashboard: {
      title: 'Contract Analysis Dashboard',
      overallRisk: 'Overall Risk Score',
      totalRisks: 'Total Risks',
      missingClauses: 'Missing Clauses',
      completionScore: 'Completion Score',
      criticalIssues: 'Critical Issues',
      domainRiskScores: 'Domain Risk Scores',
      riskSeverityDistribution: 'Risk Severity Distribution',
      topRiskTypes: 'Top Risk Types',
      extractedClauses: 'Extracted Clauses by Domain',
      missingCriticalClauses: 'Missing Critical Clauses',
      riskSeverityHeatmap: 'Risk Severity Heatmap',
      lowRisk: 'Low Risk',
      highRisk: 'High Risk'
    },

    // Risk Levels
    risk: {
      overall: 'Overall Risk Score',
      criticalRisk: 'CRITICAL RISK',
      highRisk: 'HIGH RISK',
      mediumRisk: 'MEDIUM RISK',
      lowRisk: 'LOW RISK',
      critical: 'Critical',
      high: 'High',
      medium: 'Medium',
      low: 'Low',
      domainBreakdown: 'Domain Risk Breakdown',
      complianceRisk: 'Compliance Risk',
      financialRisk: 'Financial Risk',
      legalRisk: 'Legal Risk',
      operationalRisk: 'Operational Risk',
      severityDistribution: 'Risk Severity Distribution',
      riskCount: 'risks',
      scoringMethodology: 'Scoring Methodology',
      riskLevelGuide: 'Risk Level Guide'
    },

    // Missing Clauses
    missingClauses: {
      title: 'Missing Critical Clauses',
      allPresent: 'All Critical Clauses Present!',
      allPresentDesc: 'This contract includes all essential clauses for comprehensive protection.',
      completeness: 'Completeness',
      complete: 'Complete',
      criticalMissing: 'Critical Missing',
      highPriority: 'High Priority',
      mediumPriority: 'Medium Priority',
      totalMissing: 'Total Missing',
      category: 'Category',
      whyItMatters: 'Why It Matters',
      recommendation: 'Recommendation',
      importance: 'Importance'
    },

    // Domains
    domains: {
      compliance: 'Compliance',
      financial: 'Financial',
      legal: 'Legal',
      operational: 'Operational',
      finance: 'Finance',
      operations: 'Operations'
    },

    // Analysis Sections
    analysis: {
      executiveSummary: 'Executive Summary',
      keyFindings: 'Key Findings',
      extractedClauses: 'Extracted Clauses',
      identifiedRisks: 'Identified Risks',
      agentDiscussions: 'Agent Discussions',
      complianceAnalysis: 'Compliance Analysis',
      financeAnalysis: 'Finance Analysis',
      legalAnalysis: 'Legal Analysis',
      operationsAnalysis: 'Operations Analysis',
      recommendations: 'Recommendations',
      discussionTopic: 'Discussion',
      completed: 'Completed'
    },

    // Report Export
    report: {
      title: 'Export Report',
      selectTone: 'Select Report Tone',
      selectFormat: 'Select Format',
      download: 'Download Report',
      generating: 'Generating report...',
      tones: {
        professional: 'Professional',
        technical: 'Technical',
        executive: 'Executive',
        detailed: 'Detailed'
      },
      formats: {
        markdown: 'Markdown',
        html: 'HTML',
        json: 'JSON'
      },
      toneHelp: {
        professional: 'Balanced tone for business stakeholders',
        technical: 'Detailed technical language for legal experts',
        executive: 'Concise high-level overview for executives',
        detailed: 'Comprehensive analysis with full details'
      }
    },

    // Common Actions
    actions: {
      upload: 'Upload',
      analyze: 'Analyze',
      download: 'Download',
      export: 'Export',
      cancel: 'Cancel',
      close: 'Close',
      save: 'Save',
      delete: 'Delete',
      edit: 'Edit',
      view: 'View',
      back: 'Back',
      next: 'Next',
      submit: 'Submit',
      reset: 'Reset',
      search: 'Search',
      filter: 'Filter',
      sort: 'Sort'
    },

    // Status Messages
    messages: {
      success: 'Operation completed successfully',
      error: 'An error occurred',
      loading: 'Loading...',
      noData: 'No data available',
      processingFile: 'Processing file...',
      analysisComplete: 'Analysis complete!',
      saved: 'Saved successfully',
      deleted: 'Deleted successfully'
    },

    // Clause Types
    clauseTypes: {
      payment: 'Payment',
      termination: 'Termination',
      liability: 'Liability',
      confidentiality: 'Confidentiality',
      warranty: 'Warranty',
      indemnification: 'Indemnification',
      jurisdiction: 'Jurisdiction',
      forceMajeure: 'Force Majeure',
      general: 'General'
    },

    // Severity Badges
    severity: {
      critical: 'CRITICAL',
      high: 'HIGH',
      medium: 'MEDIUM',
      low: 'LOW'
    },

    // Contract Chat
    chat: {
      title: 'Contract Assistant',
      subtitle: 'Ask questions about your contract',
      welcome: 'Hi! I\'m your contract assistant. Ask me anything about the analyzed contract.',
      placeholder: 'Ask a question about the contract...',
      suggestedQuestions: 'Suggested Questions',
      sources: 'Sources',
      error: 'Sorry, I encountered an error. Please try again.',
      confidence: {
        label: 'Confidence',
        high: 'High',
        medium: 'Medium',
        low: 'Low'
      }
    }
  },

  ta: {
    // Tamil Translations
    appName: 'ClauseAI',
    tagline: 'AI உதவியுடன் சட்ட ஒப்பந்த பகுப்பாய்வு',

    nav: {
      home: 'முகப்பு',
      dashboard: 'டாஷ்போர்டு',
      analyze: 'ஒப்பந்த பகுப்பாய்வு',
      reports: 'அறிக்கைகள்',
      settings: 'அமைப்புகள்'
    },

    upload: {
      title: 'ஒப்பந்தத்தை பதிவேற்றவும்',
      dragDrop: 'உங்கள் ஒப்பந்தத்தை இங்கே இழுத்து விடவும்',
      or: 'அல்லது',
      browse: 'கோப்புகளை உலாவவும்',
      supported: 'ஆதரிக்கப்படும் வடிவங்கள்: PDF, DOCX, TXT',
      maxSize: 'அதிகபட்ச அளவு: 10MB',
      analyzing: 'ஒப்பந்தத்தை பகுப்பாய்வு செய்கிறது...',
      pleaseWait: 'எங்கள் AI முகவர்கள் உங்கள் ஒப்பந்தத்தை பகுப்பாய்வு செய்யும் வரை காத்திருக்கவும்',
      error: 'பதிவேற்றம் தோல்வியடைந்தது. மீண்டும் முயற்சிக்கவும்.',
      selectFile: 'பதிவேற்ற ஒரு கோப்பைத் தேர்ந்தெடுக்கவும்'
    },

    dashboard: {
      title: 'ஒப்பந்த பகுப்பாய்வு டாஷ்போர்டு',
      overallRisk: 'ஒட்டுமொத்த இடர் மதிப்பெண்',
      totalRisks: 'மொத்த இடர்கள்',
      missingClauses: 'காணாமல் உள்ள விதிமுறைகள்',
      completionScore: 'நிறைவு மதிப்பெண்',
      criticalIssues: 'முக்கிய பிரச்சினைகள்',
      domainRiskScores: 'களம் இடர் மதிப்பெண்கள்',
      riskSeverityDistribution: 'இடர் தீவிர விநியோகம்',
      topRiskTypes: 'முதன்மை இடர் வகைகள்',
      extractedClauses: 'களம் மூலம் பிரித்தெடுக்கப்பட்ட விதிமுறைகள்',
      missingCriticalClauses: 'காணாமல் உள்ள முக்கிய விதிமுறைகள்',
      riskSeverityHeatmap: 'இடர் தீவிர வெப்ப வரைபடம்',
      lowRisk: 'குறைந்த இடர்',
      highRisk: 'அதிக இடர்'
    },

    risk: {
      overall: 'ஒட்டுமொத்த இடர் மதிப்பெண்',
      criticalRisk: 'முக்கிய இடர்',
      highRisk: 'அதிக இடர்',
      mediumRisk: 'நடுத்தர இடர்',
      lowRisk: 'குறைந்த இடர்',
      critical: 'முக்கியமான',
      high: 'உயர்',
      medium: 'நடுத்தரம்',
      low: 'குறைந்த',
      domainBreakdown: 'களம் இடர் பிரிவு',
      complianceRisk: 'இணக்க இடர்',
      financialRisk: 'நிதி இடர்',
      legalRisk: 'சட்ட இடர்',
      operationalRisk: 'செயல்பாட்டு இடர்',
      severityDistribution: 'இடர் தீவிர விநியோகம்',
      riskCount: 'இடர்கள்',
      scoringMethodology: 'மதிப்பெண் முறை',
      riskLevelGuide: 'இடர் நிலை வழிகாட்டி'
    },

    missingClauses: {
      title: 'காணாமல் உள்ள முக்கிய விதிமுறைகள்',
      allPresent: 'அனைத்து முக்கிய விதிமுறைகளும் உள்ளன!',
      allPresentDesc: 'இந்த ஒப்பந்தம் விரிவான பாதுகாப்புக்கு அனைத்து அத்தியாவசிய விதிமுறைகளையும் உள்ளடக்கியது.',
      completeness: 'முழுமை',
      complete: 'முழுமையான',
      criticalMissing: 'முக்கிய காணவில்லை',
      highPriority: 'உயர் முன்னுரிமை',
      mediumPriority: 'நடுத்தர முன்னுரிமை',
      totalMissing: 'மொத்த காணவில்லை',
      category: 'வகை',
      whyItMatters: 'ஏன் இது முக்கியம்',
      recommendation: 'பரிந்துரை',
      importance: 'முக்கியத்துவம்'
    },

    domains: {
      compliance: 'இணக்கம்',
      financial: 'நிதி',
      legal: 'சட்டம்',
      operational: 'செயல்பாட்டு',
      finance: 'நிதி',
      operations: 'செயல்பாடுகள்'
    },

    analysis: {
      executiveSummary: 'நிர்வாக சுருக்கம்',
      keyFindings: 'முக்கிய கண்டுபிடிப்புகள்',
      extractedClauses: 'பிரித்தெடுக்கப்பட்ட விதிமுறைகள்',
      identifiedRisks: 'அடையாளம் காணப்பட்ட இடர்கள்',
      agentDiscussions: 'முகவர் விவாதங்கள்',
      complianceAnalysis: 'இணக்க பகுப்பாய்வு',
      financeAnalysis: 'நிதி பகுப்பாய்வு',
      legalAnalysis: 'சட்ட பகுப்பாய்வு',
      operationsAnalysis: 'செயல்பாட்டு பகுப்பாய்வு',
      recommendations: 'பரிந்துரைகள்',
      discussionTopic: 'விவாதம்',
      completed: 'நிறைவு'
    },

    report: {
      title: 'அறிக்கை ஏற்றுமதி',
      selectTone: 'அறிக்கை தொனியைத் தேர்ந்தெடுக்கவும்',
      selectFormat: 'வடிவத்தைத் தேர்ந்தெடுக்கவும்',
      download: 'அறிக்கையை பதிவிறக்கவும்',
      generating: 'அறிக்கை உருவாக்கப்படுகிறது...',
      tones: {
        professional: 'தொழில்முறை',
        technical: 'தொழில்நுட்ப',
        executive: 'நிர்வாக',
        detailed: 'விரிவான'
      },
      formats: {
        markdown: 'மார்க்டவுன்',
        html: 'HTML',
        json: 'JSON'
      },
      toneHelp: {
        professional: 'வணிக பங்குதாரர்களுக்கான சமநிலையான தொனி',
        technical: 'சட்ட நிபுணர்களுக்கான விரிவான தொழில்நுட்ப மொழி',
        executive: 'நிர்வாகிகளுக்கான சுருக்கமான உயர்நிலை மேலோட்டம்',
        detailed: 'முழு விவரங்களுடன் விரிவான பகுப்பாய்வு'
      }
    },

    actions: {
      upload: 'பதிவேற்றவும்',
      analyze: 'பகுப்பாய்வு செய்யவும்',
      download: 'பதிவிறக்கவும்',
      export: 'ஏற்றுமதி',
      cancel: 'ரத்து செய்',
      close: 'மூடு',
      save: 'சேமி',
      delete: 'நீக்கு',
      edit: 'திருத்து',
      view: 'பார்க்கவும்',
      back: 'பின்',
      next: 'அடுத்தது',
      submit: 'சமர்ப்பிக்கவும்',
      reset: 'மீட்டமை',
      search: 'தேடு',
      filter: 'வடிகட்டி',
      sort: 'வரிசைப்படுத்து'
    },

    messages: {
      success: 'செயல்பாடு வெற்றிகரமாக முடிந்தது',
      error: 'பிழை ஏற்பட்டது',
      loading: 'ஏற்றுகிறது...',
      noData: 'தரவு இல்லை',
      processingFile: 'கோப்பை செயலாக்குகிறது...',
      analysisComplete: 'பகுப்பாய்வு முடிந்தது!',
      saved: 'வெற்றிகரமாக சேமிக்கப்பட்டது',
      deleted: 'வெற்றிகரமாக நீக்கப்பட்டது'
    },

    clauseTypes: {
      payment: 'கட்டணம்',
      termination: 'முடிவுறுத்தல்',
      liability: 'பொறுப்பு',
      confidentiality: 'இரகசியத்தன்மை',
      warranty: 'உத்தரவாதம்',
      indemnification: 'இழப்பீடு',
      jurisdiction: 'அதிகார எல்லை',
      forceMajeure: 'மேலதிக சக்தி',
      general: 'பொது'
    },

    severity: {
      critical: 'முக்கியமான',
      high: 'உயர்',
      medium: 'நடுத்தரம்',
      low: 'குறைந்த'
    },

    chat: {
      title: 'ஒப்பந்த உதவியாளர்',
      subtitle: 'உங்கள் ஒப்பந்தத்தைப் பற்றி கேள்விகள் கேளுங்கள்',
      welcome: 'வணக்கம்! நான் உங்கள் ஒப்பந்த உதவியாளர். பகுப்பாய்வு செய்யப்பட்ட ஒப்பந்தத்தைப் பற்றி எதையும் என்னிடம் கேளுங்கள்.',
      placeholder: 'ஒப்பந்தத்தைப் பற்றி ஒரு கேள்வியைக் கேளுங்கள்...',
      suggestedQuestions: 'பரிந்துரைக்கப்பட்ட கேள்விகள்',
      sources: 'ஆதாரங்கள்',
      error: 'மன்னிக்கவும், நான் ஒரு பிழையை சந்தித்தேன். மீண்டும் முயற்சிக்கவும்.',
      confidence: {
        label: 'நம்பிக்கை',
        high: 'உயர்',
        medium: 'நடுத்தரம்',
        low: 'குறைந்த'
      }
    }
  },

  hi: {
    // Hindi Translations
    appName: 'ClauseAI',
    tagline: 'AI-संचालित कानूनी अनुबंध विश्लेषक',

    nav: {
      home: 'होम',
      dashboard: 'डैशबोर्ड',
      analyze: 'अनुबंध विश्लेषण',
      reports: 'रिपोर्ट',
      settings: 'सेटिंग्स'
    },

    upload: {
      title: 'अनुबंध अपलोड करें',
      dragDrop: 'अपना अनुबंध यहां खींचें और छोड़ें',
      or: 'या',
      browse: 'फ़ाइलें ब्राउज़ करें',
      supported: 'समर्थित प्रारूप: PDF, DOCX, TXT',
      maxSize: 'अधिकतम आकार: 10MB',
      analyzing: 'अनुबंध का विश्लेषण किया जा रहा है...',
      pleaseWait: 'कृपया प्रतीक्षा करें जब हमारे AI एजेंट आपके अनुबंध का विश्लेषण करते हैं',
      error: 'अपलोड विफल हुआ। कृपया पुनः प्रयास करें।',
      selectFile: 'कृपया अपलोड करने के लिए एक फ़ाइल चुनें'
    },

    dashboard: {
      title: 'अनुबंध विश्लेषण डैशबोर्ड',
      overallRisk: 'समग्र जोखिम स्कोर',
      totalRisks: 'कुल जोखिम',
      missingClauses: 'लापता खंड',
      completionScore: 'पूर्णता स्कोर',
      criticalIssues: 'महत्वपूर्ण मुद्दे',
      domainRiskScores: 'डोमेन जोखिम स्कोर',
      riskSeverityDistribution: 'जोखिम गंभीरता वितरण',
      topRiskTypes: 'शीर्ष जोखिम प्रकार',
      extractedClauses: 'डोमेन द्वारा निकाले गए खंड',
      missingCriticalClauses: 'लापता महत्वपूर्ण खंड',
      riskSeverityHeatmap: 'जोखिम गंभीरता हीटमैप',
      lowRisk: 'कम जोखिम',
      highRisk: 'उच्च जोखिम'
    },

    risk: {
      overall: 'समग्र जोखिम स्कोर',
      criticalRisk: 'गंभीर जोखिम',
      highRisk: 'उच्च जोखिम',
      mediumRisk: 'मध्यम जोखिम',
      lowRisk: 'कम जोखिम',
      critical: 'गंभीर',
      high: 'उच्च',
      medium: 'मध्यम',
      low: 'कम',
      domainBreakdown: 'डोमेन जोखिम विभाजन',
      complianceRisk: 'अनुपालन जोखिम',
      financialRisk: 'वित्तीय जोखिम',
      legalRisk: 'कानूनी जोखिम',
      operationalRisk: 'परिचालन जोखिम',
      severityDistribution: 'जोखिम गंभीरता वितरण',
      riskCount: 'जोखिम',
      scoringMethodology: 'स्कोरिंग पद्धति',
      riskLevelGuide: 'जोखिम स्तर गाइड'
    },

    missingClauses: {
      title: 'लापता महत्वपूर्ण खंड',
      allPresent: 'सभी महत्वपूर्ण खंड मौजूद हैं!',
      allPresentDesc: 'इस अनुबंध में व्यापक सुरक्षा के लिए सभी आवश्यक खंड शामिल हैं।',
      completeness: 'पूर्णता',
      complete: 'पूर्ण',
      criticalMissing: 'गंभीर लापता',
      highPriority: 'उच्च प्राथमिकता',
      mediumPriority: 'मध्यम प्राथमिकता',
      totalMissing: 'कुल लापता',
      category: 'श्रेणी',
      whyItMatters: 'यह क्यों मायने रखता है',
      recommendation: 'सिफारिश',
      importance: 'महत्व'
    },

    domains: {
      compliance: 'अनुपालन',
      financial: 'वित्तीय',
      legal: 'कानूनी',
      operational: 'परिचालन',
      finance: 'वित्त',
      operations: 'संचालन'
    },

    analysis: {
      executiveSummary: 'कार्यकारी सारांश',
      keyFindings: 'मुख्य निष्कर्ष',
      extractedClauses: 'निकाले गए खंड',
      identifiedRisks: 'पहचाने गए जोखिम',
      agentDiscussions: 'एजेंट चर्चा',
      complianceAnalysis: 'अनुपालन विश्लेषण',
      financeAnalysis: 'वित्त विश्लेषण',
      legalAnalysis: 'कानूनी विश्लेषण',
      operationsAnalysis: 'संचालन विश्लेषण',
      recommendations: 'सिफारिशें',
      discussionTopic: 'चर्चा',
      completed: 'पूर्ण'
    },

    report: {
      title: 'रिपोर्ट निर्यात',
      selectTone: 'रिपोर्ट टोन चुनें',
      selectFormat: 'प्रारूप चुनें',
      download: 'रिपोर्ट डाउनलोड करें',
      generating: 'रिपोर्ट बनाई जा रही है...',
      tones: {
        professional: 'पेशेवर',
        technical: 'तकनीकी',
        executive: 'कार्यकारी',
        detailed: 'विस्तृत'
      },
      formats: {
        markdown: 'मार्कडाउन',
        html: 'HTML',
        json: 'JSON'
      },
      toneHelp: {
        professional: 'व्यवसाय हितधारकों के लिए संतुलित टोन',
        technical: 'कानूनी विशेषज्ञों के लिए विस्तृत तकनीकी भाषा',
        executive: 'अधिकारियों के लिए संक्षिप्त उच्च-स्तरीय अवलोकन',
        detailed: 'पूर्ण विवरण के साथ व्यापक विश्लेषण'
      }
    },

    actions: {
      upload: 'अपलोड करें',
      analyze: 'विश्लेषण करें',
      download: 'डाउनलोड करें',
      export: 'निर्यात',
      cancel: 'रद्द करें',
      close: 'बंद करें',
      save: 'सहेजें',
      delete: 'हटाएं',
      edit: 'संपादित करें',
      view: 'देखें',
      back: 'पीछे',
      next: 'अगला',
      submit: 'जमा करें',
      reset: 'रीसेट करें',
      search: 'खोजें',
      filter: 'फ़िल्टर',
      sort: 'क्रमबद्ध करें'
    },

    messages: {
      success: 'ऑपरेशन सफलतापूर्वक पूर्ण हुआ',
      error: 'एक त्रुटि हुई',
      loading: 'लोड हो रहा है...',
      noData: 'कोई डेटा उपलब्ध नहीं',
      processingFile: 'फ़ाइल प्रोसेस हो रही है...',
      analysisComplete: 'विश्लेषण पूर्ण!',
      saved: 'सफलतापूर्वक सहेजा गया',
      deleted: 'सफलतापूर्वक हटाया गया'
    },

    clauseTypes: {
      payment: 'भुगतान',
      termination: 'समाप्ति',
      liability: 'दायित्व',
      confidentiality: 'गोपनीयता',
      warranty: 'वारंटी',
      indemnification: 'क्षतिपूर्ति',
      jurisdiction: 'अधिकार क्षेत्र',
      forceMajeure: 'फोर्स मजेर',
      general: 'सामान्य'
    },

    severity: {
      critical: 'गंभीर',
      high: 'उच्च',
      medium: 'मध्यम',
      low: 'कम'
    }
  },

  te: {
    // Telugu Translations
    appName: 'ClauseAI',
    tagline: 'AI-ఆధారిత చట్టపరమైన ఒప్పంద విశ్లేషకుడు',

    nav: {
      home: 'హోమ్',
      dashboard: 'డాష్‌బోర్డ్',
      analyze: 'ఒప్పంద విశ్లేషణ',
      reports: 'నివేదికలు',
      settings: 'సెట్టింగులు'
    },

    upload: {
      title: 'ఒప్పందాన్ని అప్‌లోడ్ చేయండి',
      dragDrop: 'మీ ఒప్పందాన్ని ఇక్కడ లాగి వదలండి',
      or: 'లేదా',
      browse: 'ఫైల్‌లను బ్రౌజ్ చేయండి',
      supported: 'మద్దతు ఇచ్చే ఫార్మాట్‌లు: PDF, DOCX, TXT',
      maxSize: 'గరిష్ట పరిమాణం: 10MB',
      analyzing: 'ఒప్పందాన్ని విశ్లేషిస్తోంది...',
      pleaseWait: 'మా AI ఏజెంట్‌లు మీ ఒప్పందాన్ని విశ్లేషిస్తున్నప్పుడు దయచేసి వేచి ఉండండి',
      error: 'అప్‌లోడ్ విఫలమైంది. దయచేసి మళ్లీ ప్రయత్నించండి.',
      selectFile: 'దయచేసి అప్‌లోడ్ చేయడానికి ఒక ఫైల్‌ను ఎంచుకోండి'
    },

    dashboard: {
      title: 'ఒప్పంద విశ్లేషణ డాష్‌బోర్డ్',
      overallRisk: 'మొత్తం రిస్క్ స్కోర్',
      totalRisks: 'మొత్తం రిస్క్‌లు',
      missingClauses: 'తప్పిపోయిన నిబంధనలు',
      completionScore: 'పూర్తి స్కోర్',
      criticalIssues: 'క్లిష్టమైన సమస్యలు',
      domainRiskScores: 'డొమైన్ రిస్క్ స్కోర్‌లు',
      riskSeverityDistribution: 'రిస్క్ తీవ్రత పంపిణీ',
      topRiskTypes: 'టాప్ రిస్క్ రకాలు',
      extractedClauses: 'డొమైన్ ద్వారా సేకరించిన నిబంధనలు',
      missingCriticalClauses: 'తప్పిపోయిన క్లిష్టమైన నిబంధనలు',
      riskSeverityHeatmap: 'రిస్క్ తీవ్రత హీట్‌మ్యాప్',
      lowRisk: 'తక్కువ రిస్క్',
      highRisk: 'అధిక రిస్క్'
    },

    risk: {
      overall: 'మొత్తం రిస్క్ స్కోర్',
      criticalRisk: 'క్లిష్టమైన రిస్క్',
      highRisk: 'అధిక రిస్క్',
      mediumRisk: 'మధ్యస్థ రిస్క్',
      lowRisk: 'తక్కువ రిస్క్',
      critical: 'క్లిష్టమైన',
      high: 'అధిక',
      medium: 'మధ్యస్థ',
      low: 'తక్కువ',
      domainBreakdown: 'డొమైన్ రిస్క్ విభజన',
      complianceRisk: 'సమ్మతి రిస్క్',
      financialRisk: 'ఆర్థిక రిస్క్',
      legalRisk: 'చట్టపరమైన రిస్క్',
      operationalRisk: 'కార్యాచరణ రిస్క్',
      severityDistribution: 'రిస్క్ తీవ్రత పంపిణీ',
      riskCount: 'రిస్క్‌లు',
      scoringMethodology: 'స్కోరింగ్ పద్ధతి',
      riskLevelGuide: 'రిస్క్ స్థాయి గైడ్'
    },

    missingClauses: {
      title: 'తప్పిపోయిన క్లిష్టమైన నిబంధనలు',
      allPresent: 'అన్ని క్లిష్టమైన నిబంధనలు ఉన్నాయి!',
      allPresentDesc: 'ఈ ఒప్పందం సమగ్ర రక్షణ కోసం అన్ని అవసరమైన నిబంధనలను కలిగి ఉంది.',
      completeness: 'పూర్తిత',
      complete: 'పూర్తి',
      criticalMissing: 'క్లిష్టమైన తప్పిపోయినవి',
      highPriority: 'అధిక ప్రాధాన్యత',
      mediumPriority: 'మధ్యస్థ ప్రాధాన్యత',
      totalMissing: 'మొత్తం తప్పిపోయినవి',
      category: 'వర్గం',
      whyItMatters: 'ఇది ఎందుకు ముఖ్యం',
      recommendation: 'సిఫార్సు',
      importance: 'ప్రాముఖ్యత'
    },

    domains: {
      compliance: 'సమ్మతి',
      financial: 'ఆర్థిక',
      legal: 'చట్టపరమైన',
      operational: 'కార్యాచరణ',
      finance: 'ఆర్థిక',
      operations: 'కార్యకలాపాలు'
    },

    analysis: {
      executiveSummary: 'ఎగ్జిక్యూటివ్ సారాంశం',
      keyFindings: 'ముఖ్య కనుగొనడాలు',
      extractedClauses: 'సేకరించిన నిబంధనలు',
      identifiedRisks: 'గుర్తించిన రిస్క్‌లు',
      agentDiscussions: 'ఏజెంట్ చర్చలు',
      complianceAnalysis: 'సమ్మతి విశ్లేషణ',
      financeAnalysis: 'ఆర్థిక విశ్లేషణ',
      legalAnalysis: 'చట్టపరమైన విశ్లేషణ',
      operationsAnalysis: 'కార్యకలాపాల విశ్లేషణ',
      recommendations: 'సిఫార్సులు',
      discussionTopic: 'చర్చ',
      completed: 'పూర్తయింది'
    },

    report: {
      title: 'నివేదిక ఎగుమతి',
      selectTone: 'నివేదిక టోన్ ఎంచుకోండి',
      selectFormat: 'ఫార్మాట్ ఎంచుకోండి',
      download: 'నివేదిక డౌన్‌లోడ్ చేయండి',
      generating: 'నివేదిక రూపొందిస్తోంది...',
      tones: {
        professional: 'వృత్తిపరమైన',
        technical: 'సాంకేతిక',
        executive: 'ఎగ్జిక్యూటివ్',
        detailed: 'వివరణాత్మక'
      },
      formats: {
        markdown: 'మార్క్‌డౌన్',
        html: 'HTML',
        json: 'JSON'
      },
      toneHelp: {
        professional: 'వ్యాపార వాటాదారులకు సమతుల్యమైన టోన్',
        technical: 'చట్టపరమైన నిపుణులకు వివరణాత్మక సాంకేతిక భాష',
        executive: 'ఎగ్జిక్యూటివ్‌లకు సంక్షిప్త ఉన్నత-స్థాయి అవలోకనం',
        detailed: 'పూర్తి వివరాలతో సమగ్ర విశ్లేషణ'
      }
    },

    actions: {
      upload: 'అప్‌లోడ్ చేయండి',
      analyze: 'విశ్లేషించండి',
      download: 'డౌన్‌లోడ్ చేయండి',
      export: 'ఎగుమతి',
      cancel: 'రద్దు చేయండి',
      close: 'మూసివేయండి',
      save: 'సేవ్ చేయండి',
      delete: 'తొలగించండి',
      edit: 'సవరించండి',
      view: 'వీక్షించండి',
      back: 'వెనుకకు',
      next: 'తదుపరి',
      submit: 'సమర్పించండి',
      reset: 'రీసెట్ చేయండి',
      search: 'శోధించండి',
      filter: 'ఫిల్టర్',
      sort: 'క్రమబద్ధీకరించండి'
    },

    messages: {
      success: 'ఆపరేషన్ విజయవంతంగా పూర్తయింది',
      error: 'ఒక లోపం సంభవించింది',
      loading: 'లోడ్ అవుతోంది...',
      noData: 'డేటా అందుబాటులో లేదు',
      processingFile: 'ఫైల్ ప్రాసెస్ అవుతోంది...',
      analysisComplete: 'విశ్లేషణ పూర్తయింది!',
      saved: 'విజయవంతంగా సేవ్ చేయబడింది',
      deleted: 'విజయవంతంగా తొలగించబడింది'
    },

    clauseTypes: {
      payment: 'చెల్లింపు',
      termination: 'ముగింపు',
      liability: 'బాధ్యత',
      confidentiality: 'గోప్యత',
      warranty: 'వారంటీ',
      indemnification: 'నష్టపరిహారం',
      jurisdiction: 'అధికార పరిధి',
      forceMajeure: 'ఫోర్స్ మజెర్',
      general: 'సాధారణ'
    },

    severity: {
      critical: 'క్లిష్టమైన',
      high: 'అధిక',
      medium: 'మధ్యస్థ',
      low: 'తక్కువ'
    }
  },

  ml: {
    // Malayalam Translations
    appName: 'ClauseAI',
    tagline: 'AI-പവർഡ് നിയമ കരാർ വിശകലനം',

    nav: {
      home: 'ഹോം',
      dashboard: 'ഡാഷ്ബോർഡ്',
      analyze: 'കരാർ വിശകലനം',
      reports: 'റിപ്പോർട്ടുകൾ',
      settings: 'ക്രമീകരണങ്ങൾ'
    },

    upload: {
      title: 'കരാർ അപ്‌ലോഡ് ചെയ്യുക',
      dragDrop: 'നിങ്ങളുടെ കരാർ ഇവിടെ വലിച്ചിടുക',
      or: 'അല്ലെങ്കിൽ',
      browse: 'ഫയലുകൾ ബ്രൗസ് ചെയ്യുക',
      supported: 'പിന്തുണയ്ക്കുന്ന ഫോർമാറ്റുകൾ: PDF, DOCX, TXT',
      maxSize: 'പരമാവധി വലുപ്പം: 10MB',
      analyzing: 'കരാർ വിശകലനം ചെയ്യുന്നു...',
      pleaseWait: 'ഞങ്ങളുടെ AI ഏജൻറുകൾ നിങ്ങളുടെ കരാർ വിശകലനം ചെയ്യുമ്പോൾ കാത്തിരിക്കുക',
      error: 'അപ്‌ലോഡ് പരാജയപ്പെട്ടു. വീണ്ടും ശ്രമിക്കുക.',
      selectFile: 'ദയവായി അപ്‌ലോഡ് ചെയ്യാൻ ഒരു ഫയൽ തിരഞ്ഞെടുക്കുക'
    },

    dashboard: {
      title: 'കരാർ വിശകലന ഡാഷ്ബോർഡ്',
      overallRisk: 'മൊത്തത്തിലുള്ള റിസ്ക് സ്കോർ',
      totalRisks: 'മൊത്തം അപകടങ്ങൾ',
      missingClauses: 'നഷ്‌ടമായ വ്യവസ്ഥകൾ',
      completionScore: 'പൂർത്തീകരണ സ്കോർ',
      criticalIssues: 'ഗുരുതരമായ പ്രശ്നങ്ങൾ',
      domainRiskScores: 'ഡൊമെയ്ൻ റിസ്ക് സ്കോറുകൾ',
      riskSeverityDistribution: 'റിസ്ക് തീവ്രത വിതരണം',
      topRiskTypes: 'പ്രധാന റിസ്ക് തരങ്ങൾ',
      extractedClauses: 'ഡൊമെയ്ൻ അനുസരിച്ച് എക്സ്ട്രാക്ട് ചെയ്ത വ്യവസ്ഥകൾ',
      missingCriticalClauses: 'നഷ്‌ടമായ ഗുരുതരമായ വ്യവസ്ഥകൾ',
      riskSeverityHeatmap: 'റിസ്ക് തീവ്രത ഹീറ്റ്മാപ്പ്',
      lowRisk: 'കുറഞ്ഞ അപകടം',
      highRisk: 'ഉയർന്ന അപകടം'
    },

    risk: {
      overall: 'മൊത്തത്തിലുള്ള റിസ്ക് സ്കോർ',
      criticalRisk: 'ഗുരുതരമായ അപകടം',
      highRisk: 'ഉയർന്ന അപകടം',
      mediumRisk: 'മധ്യമ അപകടം',
      lowRisk: 'കുറഞ്ഞ അപകടം',
      critical: 'ഗുരുതരമായ',
      high: 'ഉയർന്ന',
      medium: 'മധ്യമ',
      low: 'കുറഞ്ഞ',
      domainBreakdown: 'ഡൊമെയ്ൻ റിസ്ക് വിഭജനം',
      complianceRisk: 'പാലിക്കൽ അപകടം',
      financialRisk: 'സാമ്പത്തിക അപകടം',
      legalRisk: 'നിയമപരമായ അപകടം',
      operationalRisk: 'പ്രവർത്തന അപകടം',
      severityDistribution: 'റിസ്ക് തീവ്രത വിതരണം',
      riskCount: 'അപകടങ്ങൾ',
      scoringMethodology: 'സ്കോറിംഗ് രീതി',
      riskLevelGuide: 'റിസ്ക് ലെവൽ ഗൈഡ്'
    },

    missingClauses: {
      title: 'നഷ്‌ടമായ ഗുരുതരമായ വ്യവസ്ഥകൾ',
      allPresent: 'എല്ലാ ഗുരുതരമായ വ്യവസ്ഥകളും ഉണ്ട്!',
      allPresentDesc: 'സമഗ്രമായ സംരക്ഷണത്തിനായി ഈ കരാറിൽ എല്ലാ അവശ്യ വ്യവസ്ഥകളും ഉൾപ്പെടുന്നു.',
      completeness: 'പൂർത്തീകരണം',
      complete: 'പൂർണ്ണമായ',
      criticalMissing: 'ഗുരുതരമായ നഷ്‌ടമായത്',
      highPriority: 'ഉയർന്ന മുൻഗണന',
      mediumPriority: 'മധ്യമ മുൻഗണന',
      totalMissing: 'മൊത്തം നഷ്‌ടമായത്',
      category: 'വിഭാഗം',
      whyItMatters: 'എന്തുകൊണ്ട് ഇത് പ്രധാനമാണ്',
      recommendation: 'ശുപാർശ',
      importance: 'പ്രാധാന്യം'
    },

    domains: {
      compliance: 'പാലിക്കൽ',
      financial: 'സാമ്പത്തിക',
      legal: 'നിയമപരമായ',
      operational: 'പ്രവർത്തന',
      finance: 'ധനകാര്യം',
      operations: 'പ്രവർത്തനങ്ങൾ'
    },

    analysis: {
      executiveSummary: 'എക്സിക്യൂട്ടീവ് സംഗ്രഹം',
      keyFindings: 'പ്രധാന കണ്ടെത്തലുകൾ',
      extractedClauses: 'എക്സ്ട്രാക്ട് ചെയ്ത വ്യവസ്ഥകൾ',
      identifiedRisks: 'തിരിച്ചറിഞ്ഞ അപകടങ്ങൾ',
      agentDiscussions: 'ഏജൻറ് ചർച്ചകൾ',
      complianceAnalysis: 'പാലിക്കൽ വിശകലനം',
      financeAnalysis: 'ധനകാര്യ വിശകലനം',
      legalAnalysis: 'നിയമപരമായ വിശകലനം',
      operationsAnalysis: 'പ്രവർത്തന വിശകലനം',
      recommendations: 'ശുപാർശകൾ',
      discussionTopic: 'ചർച്ച',
      completed: 'പൂർത്തിയായി'
    },

    report: {
      title: 'റിപ്പോർട്ട് കയറ്റുമതി',
      selectTone: 'റിപ്പോർട്ട് ടോൺ തിരഞ്ഞെടുക്കുക',
      selectFormat: 'ഫോർമാറ്റ് തിരഞ്ഞെടുക്കുക',
      download: 'റിപ്പോർട്ട് ഡൗൺലോഡ് ചെയ്യുക',
      generating: 'റിപ്പോർട്ട് സൃഷ്ടിക്കുന്നു...',
      tones: {
        professional: 'പ്രൊഫഷണൽ',
        technical: 'സാങ്കേതിക',
        executive: 'എക്സിക്യൂട്ടീവ്',
        detailed: 'വിശദമായ'
      },
      formats: {
        markdown: 'മാർക്ക്ഡൗൺ',
        html: 'HTML',
        json: 'JSON'
      },
      toneHelp: {
        professional: 'ബിസിനസ് പങ്കാളികൾക്കുള്ള സമതുലിതമായ ടോൺ',
        technical: 'നിയമ വിദഗ്ധർക്കുള്ള വിശദമായ സാങ്കേതിക ഭാഷ',
        executive: 'എക്സിക്യൂട്ടീവുകൾക്ക് സംക്ഷിപ്ത ഉയർന്ന തല അവലോകനം',
        detailed: 'പൂർണ്ണ വിശദാംശങ്ങളോടെ സമഗ്രമായ വിശകലനം'
      }
    },

    actions: {
      upload: 'അപ്‌ലോഡ് ചെയ്യുക',
      analyze: 'വിശകലനം ചെയ്യുക',
      download: 'ഡൗൺലോഡ് ചെയ്യുക',
      export: 'കയറ്റുമതി',
      cancel: 'റദ്ദാക്കുക',
      close: 'അടയ്ക്കുക',
      save: 'സംരക്ഷിക്കുക',
      delete: 'ഇല്ലാതാക്കുക',
      edit: 'എഡിറ്റ് ചെയ്യുക',
      view: 'കാണുക',
      back: 'തിരികെ',
      next: 'അടുത്തത്',
      submit: 'സമർപ്പിക്കുക',
      reset: 'റീസെറ്റ് ചെയ്യുക',
      search: 'തിരയുക',
      filter: 'ഫിൽട്ടർ',
      sort: 'അടുക്കുക'
    },

    messages: {
      success: 'പ്രവർത്തനം വിജയകരമായി പൂർത്തിയായി',
      error: 'ഒരു പിശക് സംഭവിച്ചു',
      loading: 'ലോഡ് ചെയ്യുന്നു...',
      noData: 'ഡാറ്റ ലഭ്യമല്ല',
      processingFile: 'ഫയൽ പ്രോസസ്സ് ചെയ്യുന്നു...',
      analysisComplete: 'വിശകലനം പൂർത്തിയായി!',
      saved: 'വിജയകരമായി സംരക്ഷിച്ചു',
      deleted: 'വിജയകരമായി ഇല്ലാതാക്കി'
    },

    clauseTypes: {
      payment: 'പേയ്മെന്റ്',
      termination: 'അവസാനിപ്പിക്കൽ',
      liability: 'ബാധ്യത',
      confidentiality: 'രഹസ്യസ്വഭാവം',
      warranty: 'വാറന്റി',
      indemnification: 'നഷ്ടപരിഹാരം',
      jurisdiction: 'അധികാര പരിധി',
      forceMajeure: 'ഫോഴ്സ് മജേർ',
      general: 'പൊതുവായ'
    },

    severity: {
      critical: 'ഗുരുതരമായ',
      high: 'ഉയർന്ന',
      medium: 'മധ്യമ',
      low: 'കുറഞ്ഞ'
    }
  }
};

export default translations;
