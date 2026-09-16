"use client";

import React, { useState } from 'react';
import { 
  Leaf, 
  FlaskConical, 
  Pill, 
  Sparkles, 
  Apple, 
  Smile, 
  ArrowLeft, 
  ShieldCheck, 
  Globe2, 
  Activity, 
  Scale, 
  Send,
  BookOpen
} from 'lucide-react';

export interface WizardAnswers {
  category: string;
  categoryLabel: string;
  subDetail: string;
  ingredients: string;
  bioOrigin: string;
  evidence: string;
  objective: string;
}

interface IntakeWizardProps {
  onSubmit: (compiledProfile: string, category: string, jurisdiction: 'india' | 'international') => void;
  jurisdiction?: 'india' | 'international';
  onJurisdictionChange?: (jurisdiction: 'india' | 'international') => void;
  isLoading?: boolean;
}

export default function IntakeWizard({ onSubmit, jurisdiction = 'india', onJurisdictionChange, isLoading }: IntakeWizardProps) {
  const [step, setStep] = useState(1);
  const [answers, setAnswers] = useState<WizardAnswers>({
    category: '',
    categoryLabel: '',
    subDetail: '',
    ingredients: '',
    bioOrigin: '',
    evidence: '',
    objective: ''
  });

  const handleCategorySelect = (catKey: string, catLabel: string) => {
    setAnswers(prev => ({
      ...prev,
      category: catKey,
      categoryLabel: catLabel,
      subDetail: '' // Reset step 2 on category change
    }));
    setStep(2);
  };

  const handleSubDetailSelect = (detail: string) => {
    setAnswers(prev => ({ ...prev, subDetail: detail }));
    setStep(3);
  };

  const handleBioOriginSelect = (origin: string) => {
    setAnswers(prev => ({ ...prev, bioOrigin: origin }));
    setStep(4);
  };

  const handleFinalSubmit = (evidence: string, objective: string) => {
    const finalAnswers: WizardAnswers = {
      ...answers,
      evidence,
      objective
    };
    setAnswers(finalAnswers);

    const isGlobal = objective.includes('Global') || jurisdiction === 'international';
    const targetJurisdiction: 'india' | 'international' = isGlobal ? 'international' : 'india';

    if (onJurisdictionChange) {
      onJurisdictionChange(targetJurisdiction);
    }

    // Compile into dense Innovation Disclosure Profile tailored for the selected jurisdiction
    const evaluationScope = isGlobal
      ? 'Evaluate international patentability under WIPO PCT guidelines, cross-border Access & Benefit Sharing (ABS) under Nagoya Protocol & Biological Diversity Act, international prior art search against TKDL/WIPO, and export compliance under CDSCO/AYUSH.'
      : 'Evaluate patentability under Section 3(d), Section 3(e), and Section 3(p) of the Indian Patents Act, 1970, verify Access & Benefit Sharing (ABS) requirements under the Biological Diversity Act, 2002, check Traditional Knowledge Digital Library (TKDL) conflicts, and outline the CDSCO/AYUSH regulatory licensing pathway.';

    const compiled = `INNOVATION DISCLOSURE PROFILE (${targetJurisdiction.toUpperCase()} JURISDICTION):
• Primary Product Category: ${finalAnswers.categoryLabel}
• Active Ingredients / Formulation: ${finalAnswers.ingredients.trim() || 'Herbal formulation containing traditional botanical actives'}
• Technical Formulation Detail: ${finalAnswers.subDetail}
• Biological Resource Origin (ABS): ${finalAnswers.bioOrigin}
• Scientific & Clinical Evidence: ${evidence}
• Primary Protection & Commercial Objective: ${objective}

${evaluationScope}`;

    onSubmit(compiled, finalAnswers.category, targetJurisdiction);
  };

  // Dynamic Step 2 Options based on Step 1 Category
  const getStep2Options = () => {
    switch (answers.category) {
      case 'CLASSICAL':
        return {
          title: "Schedule I Classical Text Overlap",
          subtitle: "Is this formulation mentioned verbatim in the 54 classical Ayurvedic treatises?",
          options: [
            {
              id: 'verbatim_classical',
              title: 'Exact Classical Formulation',
              desc: 'Formulation, dosage, and preparation exactly as prescribed in Charaka Samhita, Sushruta Samhita, etc. (Schedule I).',
              icon: BookOpen
            },
            {
              id: 'modified_classical',
              title: 'Modified Ratio or Process',
              desc: 'Classical ingredients used with a proprietary modification in extraction solvent, ratio, or delivery form.',
              icon: FlaskConical
            },
            {
              id: 'new_admixture',
              title: 'New Blend of Classical Herbs',
              desc: 'Novel combination of known classical herbs not found in any traditional text.',
              icon: Sparkles
            }
          ]
        };
      case 'PHYTOPHARMACEUTICAL':
        return {
          title: "Standardization & Chemical Marker Details (Rule 122E)",
          subtitle: "What level of chemical standardization and fraction purification has been achieved?",
          options: [
            {
              id: 'standardized_4markers',
              title: 'Quantified Active Markers (≥4 Markers)',
              desc: 'Standardized purified botanical extract with minimum 4 active chemical markers identified and quantified (Rule 122E).',
              icon: FlaskConical
            },
            {
              id: 'novel_extraction_solvent',
              title: 'Novel Extraction Technology / Solvent',
              desc: 'Extracted using patented/novel ultrasonic, enzymatic, or proprietary fraction separation technology.',
              icon: Activity
            },
            {
              id: 'whole_extract',
              title: 'Whole-Plant Standardized Extract',
              desc: 'Standardized for total bio-actives without isolating individual 4-marker fractions.',
              icon: Leaf
            }
          ]
        };
      case 'COSMETIC':
        return {
          title: "Cosmetic Indication & Application (Chapter III-A)",
          subtitle: "How is the formulation applied and what are the claims?",
          options: [
            {
              id: 'topical_skin_hair',
              title: 'Topical Beautification / Cleansing',
              desc: 'Applied to the human body for cleansing, beautifying, or promoting attractiveness (Ayurvedic Cosmetics Rules).',
              icon: Sparkles
            },
            {
              id: 'therapeutic_cosmetic',
              title: 'Cosmeceutical with Therapeutic Claim',
              desc: 'Herbal cosmetic claiming therapeutic dermatological relief (e.g. anti-eczema, psoriasis).',
              icon: ShieldCheck
            }
          ]
        };
      case 'AYURVEDA_AAHAR':
        return {
          title: "Ayurveda-Aahar Category (FSSAI 2022 Regulations)",
          subtitle: "What is the food/supplement format and dietary target?",
          options: [
            {
              id: 'dietary_supplement',
              title: 'Food Supplement / Rasayana Health Food',
              desc: 'Oral dietary health supplement prepared in accordance with Ayurveda-Aahar schedules and RDA limits.',
              icon: Apple
            },
            {
              id: 'functional_food',
              title: 'Functional Herbal Beverage / Food',
              desc: 'Everyday nutritional food or beverage fortified with traditional Ayurvedic botanicals.',
              icon: Leaf
            }
          ]
        };
      default:
        return {
          title: "Formulation Novelty & Modification",
          subtitle: "Specify the proprietary modification over known prior art",
          options: [
            {
              id: 'proprietary_synergy',
              title: 'Novel Polyherbal Combination',
              desc: 'Synergistic combination of botanicals engineered for specific therapeutic action.',
              icon: FlaskConical
            },
            {
              id: 'modified_molecule',
              title: 'Modified Phytochemical Entity',
              desc: 'Chemically modified natural derivative requiring clinical Phase I-III evaluation.',
              icon: Pill
            }
          ]
        };
    }
  };

  const step2Data = getStep2Options();

  return (
    <div className="wizard-container">
      {/* Wizard Header & Progress Bar */}
      <div className="wizard-header">
        <div className="wizard-title-row">
          <div className="wizard-badge">
            <Sparkles size={16} color="var(--primary-brand)" />
            <span>Interactive Guided Intake (Sahayak Wizard)</span>
          </div>
          <div className="wizard-step-counter">
            Step {step} of 4
          </div>
        </div>
        <div className="wizard-progress-track">
          <div 
            className="wizard-progress-fill"
            style={{ width: `${(step / 4) * 100}%` }}
          />
        </div>
      </div>

      {/* STEP 1: Core Product Category */}
      {step === 1 && (
        <div className="wizard-step-content animate-fade-in">
          <h3 className="wizard-step-title">What type of Ayurvedic formulation are you developing?</h3>
          <p className="wizard-step-subtitle">Select the primary category to adapt the regulatory and patentability criteria.</p>

          <div className="wizard-card-grid">
            <div 
              className={`wizard-card ${answers.category === 'CLASSICAL' ? 'selected' : ''}`}
              onClick={() => handleCategorySelect('CLASSICAL', 'Classical Ayurvedic Formulation (Schedule I)')}
            >
              <div className="wizard-card-icon"><BookOpen size={24} /></div>
              <h4>Classical Ayurveda</h4>
              <p>Formulations mentioned in the 54 classical texts (Churna, Asava, Bhasma, Taila).</p>
            </div>

            <div 
              className={`wizard-card ${answers.category === 'PROPRIETARY' ? 'selected' : ''}`}
              onClick={() => handleCategorySelect('PROPRIETARY', 'Proprietary Ayurvedic Medicine')}
            >
              <div className="wizard-card-icon"><FlaskConical size={24} /></div>
              <h4>Proprietary Ayurveda</h4>
              <p>New proprietary blends or dosage forms of known Ayurvedic herbs.</p>
            </div>

            <div 
              className={`wizard-card ${answers.category === 'PHYTOPHARMACEUTICAL' ? 'selected' : ''}`}
              onClick={() => handleCategorySelect('PHYTOPHARMACEUTICAL', 'Standardized Phytopharmaceutical (Rule 122E)')}
            >
              <div className="wizard-card-icon"><Pill size={24} /></div>
              <h4>Phytopharmaceutical</h4>
              <p>Standardized purified plant extract with minimum 4 active chemical markers.</p>
            </div>

            <div 
              className={`wizard-card ${answers.category === 'AYURVEDA_AAHAR' ? 'selected' : ''}`}
              onClick={() => handleCategorySelect('AYURVEDA_AAHAR', 'Ayurveda-Aahar / Health Food (FSSAI)')}
            >
              <div className="wizard-card-icon"><Apple size={24} /></div>
              <h4>Ayurveda-Aahar</h4>
              <p>Ayurvedic dietary supplements, functional foods, and health beverages under FSSAI.</p>
            </div>

            <div 
              className={`wizard-card ${answers.category === 'COSMETIC' ? 'selected' : ''}`}
              onClick={() => handleCategorySelect('COSMETIC', 'Ayurvedic Cosmetic (Chapter III-A)')}
            >
              <div className="wizard-card-icon"><Smile size={24} /></div>
              <h4>Ayurvedic Cosmetic</h4>
              <p>Topical skin, hair, and personal care products for cleansing and beautification.</p>
            </div>

            <div 
              className={`wizard-card ${answers.category === 'NEW_DRUG' ? 'selected' : ''}`}
              onClick={() => handleCategorySelect('NEW_DRUG', 'Novel Botanical New Drug')}
            >
              <div className="wizard-card-icon"><Activity size={24} /></div>
              <h4>Novel Botanical Drug</h4>
              <p>Highly modified molecules requiring Schedule Y clinical trials.</p>
            </div>
          </div>
        </div>
      )}

      {/* STEP 2: Adaptive Branching Question */}
      {step === 2 && (
        <div className="wizard-step-content animate-fade-in">
          <h3 className="wizard-step-title">{step2Data.title}</h3>
          <p className="wizard-step-subtitle">{step2Data.subtitle}</p>

          <div className="wizard-input-box">
            <label>Formulation Name & Key Botanical Ingredients (Optional):</label>
            <input 
              type="text" 
              placeholder="e.g. Ashwagandha (Withania somnifera) root extract + Turmeric (Curcuma longa)"
              value={answers.ingredients}
              onChange={(e) => setAnswers(prev => ({ ...prev, ingredients: e.target.value }))}
            />
          </div>

          <div className="wizard-card-grid">
            {step2Data.options.map((opt) => {
              const IconComponent = opt.icon;
              return (
                <div 
                  key={opt.id}
                  className={`wizard-card ${answers.subDetail === opt.title ? 'selected' : ''}`}
                  onClick={() => handleSubDetailSelect(opt.title)}
                >
                  <div className="wizard-card-icon"><IconComponent size={24} /></div>
                  <h4>{opt.title}</h4>
                  <p>{opt.desc}</p>
                </div>
              );
            })}
          </div>

          <div className="wizard-actions-row">
            <button className="wizard-back-btn" onClick={() => setStep(1)}>
              <ArrowLeft size={16} /> Back
            </button>
          </div>
        </div>
      )}

      {/* STEP 3: Biological Resource & Origin (ABS / NBA Compliance) */}
      {step === 3 && (
        <div className="wizard-step-content animate-fade-in">
          <h3 className="wizard-step-title">Biological Resource Sourcing & Applicant Nationality</h3>
          <p className="wizard-step-subtitle">Evaluates Access and Benefit Sharing (ABS) obligations under the Biological Diversity Act, 2002.</p>

          <div className="wizard-card-grid">
            <div 
              className={`wizard-card ${answers.bioOrigin.includes('Domestic Indian Entity') ? 'selected' : ''}`}
              onClick={() => handleBioOriginSelect('Domestic Indian Entity sourcing biological resources from Indian soil')}
            >
              <div className="wizard-card-icon"><ShieldCheck size={24} /></div>
              <h4>Indian Entity (Domestic Herbs)</h4>
              <p>Indian citizen/company sourcing biological resources from India for commercial use or patenting.</p>
            </div>

            <div 
              className={`wizard-card ${answers.bioOrigin.includes('Foreign Equity') ? 'selected' : ''}`}
              onClick={() => handleBioOriginSelect('Entity with foreign equity/directors sourcing Indian biological resources (Triggers NBA Section 3)')}
            >
              <div className="wizard-card-icon"><Globe2 size={24} /></div>
              <h4>Foreign Equity / Collaboration</h4>
              <p>Non-Indian or Indian entity with foreign equity/directors (Triggers Section 3 NBA Prior Approval).</p>
            </div>

            <div 
              className={`wizard-card ${answers.bioOrigin.includes('Value Added') ? 'selected' : ''}`}
              onClick={() => handleBioOriginSelect('Commercially purchased value-added extracts / processed ingredients')}
            >
              <div className="wizard-card-icon"><FlaskConical size={24} /></div>
              <h4>Processed Value-Added Products</h4>
              <p>Procured commercially processed extracts where biological resources are not identifiable (Exemption Check).</p>
            </div>

            <div 
              className={`wizard-card ${answers.bioOrigin.includes('Cultivated') ? 'selected' : ''}`}
              onClick={() => handleBioOriginSelect('Exclusively cultivated non-wild or imported botanical materials')}
            >
              <div className="wizard-card-icon"><Leaf size={24} /></div>
              <h4>Cultivated / Imported Botanicals</h4>
              <p>Herbs cultivated under standard GACP or legally imported from outside India.</p>
            </div>
          </div>

          <div className="wizard-actions-row">
            <button className="wizard-back-btn" onClick={() => setStep(2)}>
              <ArrowLeft size={16} /> Back
            </button>
          </div>
        </div>
      )}

      {/* STEP 4: Scientific Evidence & Objective */}
      {step === 4 && (
        <StepFourForm 
          onBack={() => setStep(3)}
          onSubmit={handleFinalSubmit}
          isLoading={isLoading}
        />
      )}
    </div>
  );
}

// Step 4 Sub-Component
function StepFourForm({ onBack, onSubmit, isLoading }: { onBack: () => void; onSubmit: (evidence: string, objective: string) => void; isLoading?: boolean }) {
  const [evidence, setEvidence] = useState('Laboratory in-vitro and in-vivo synergy data demonstrating therapeutic effect greater than sum of parts (Section 3(p) proof)');
  const [objective, setObjective] = useState('Product & Process Patent in India under Patents Act 1970 + AYUSH Manufacturing License');

  const handleSubmit = () => {
    onSubmit(evidence, objective);
  };

  return (
    <div className="wizard-step-content animate-fade-in">
      <h3 className="wizard-step-title">Scientific Validation & Legal Objective</h3>
      <p className="wizard-step-subtitle">Defines the Section 3 patentability threshold and regulatory goal.</p>

      <div style={{ marginBottom: '1.5rem' }}>
        <h4 style={{ color: 'var(--text-primary)', marginBottom: '0.75rem', fontSize: '1rem', fontWeight: 600 }}>
          1. Available Scientific / Experimental Data:
        </h4>
        <div className="wizard-card-grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))' }}>
          <div 
            className={`wizard-card ${evidence.includes('synergy') ? 'selected' : ''}`}
            onClick={() => setEvidence('Laboratory in-vitro and in-vivo synergy data demonstrating therapeutic effect greater than sum of parts (Section 3(p) proof)')}
          >
            <div className="wizard-card-icon"><Activity size={20} /></div>
            <h4>Proven Synergistic Efficacy</h4>
            <p>Data proving combination performs better than individual components.</p>
          </div>

          <div 
            className={`wizard-card ${evidence.includes('extraction') ? 'selected' : ''}`}
            onClick={() => setEvidence('Novel proprietary extraction process and physical stability/yield data')}
          >
            <div className="wizard-card-icon"><FlaskConical size={20} /></div>
            <h4>Novel Extraction Method</h4>
            <p>Process innovation (novel solvent, ultrasonic yield, temperature parameters).</p>
          </div>

          <div 
            className={`wizard-card ${evidence.includes('traditional') ? 'selected' : ''}`}
            onClick={() => setEvidence('Classical traditional usage literature and historical pharmacopoeia evidence only')}
          >
            <div className="wizard-card-icon"><BookOpen size={20} /></div>
            <h4>Traditional Use Evidence Only</h4>
            <p>Based on classical literature without novel lab synergy data.</p>
          </div>
        </div>
      </div>

      <div style={{ marginBottom: '2rem' }}>
        <h4 style={{ color: 'var(--text-primary)', marginBottom: '0.75rem', fontSize: '1rem', fontWeight: 600 }}>
          2. Primary Commercial / IP Objective:
        </h4>
        <div className="wizard-card-grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))' }}>
          <div 
            className={`wizard-card ${objective.includes('Patent in India') ? 'selected' : ''}`}
            onClick={() => setObjective('Product & Process Patent in India under Patents Act 1970 + AYUSH Manufacturing License')}
          >
            <div className="wizard-card-icon"><Scale size={20} /></div>
            <h4>Indian Patent + AYUSH License</h4>
            <p>File for Indian patent protection and obtain State AYUSH licensing.</p>
          </div>

          <div 
            className={`wizard-card ${objective.includes('Global') ? 'selected' : ''}`}
            onClick={() => setObjective('Global International Patent via WIPO PCT & Nagoya Protocol compliance')}
          >
            <div className="wizard-card-icon"><Globe2 size={20} /></div>
            <h4>Global PCT / WIPO Filing</h4>
            <p>International patent filing with cross-border ABS compliance.</p>
          </div>

          <div 
            className={`wizard-card ${objective.includes('Trademark') ? 'selected' : ''}`}
            onClick={() => setObjective('Brand Trademark, Trade Secret Protection & FSSAI / AYUSH Compliance')}
          >
            <div className="wizard-card-icon"><ShieldCheck size={20} /></div>
            <h4>Trademark & Trade Secret</h4>
            <p>Protect commercial formulation as a trade secret and brand name.</p>
          </div>
        </div>
      </div>

      <div className="wizard-actions-row" style={{ justifyContent: 'space-between' }}>
        <button className="wizard-back-btn" onClick={onBack} disabled={isLoading}>
          <ArrowLeft size={16} /> Back
        </button>
        <button className="wizard-submit-btn" onClick={handleSubmit} disabled={isLoading}>
          {isLoading ? (
            <span>Analyzing 36k Legal Corpus...</span>
          ) : (
            <>
              <span>Compile & Run Multi-Agent Analysis</span>
              <Send size={18} />
            </>
          )}
        </button>
      </div>
    </div>
  );
}
