"""
LLM-as-Judge Evaluator for Arabic Customer Service Conversations

Uses an LLM to evaluate conversation quality across multiple dimensions.
"""

import json
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from models.base_model import BaseModel
from scenarios.scenario_loader import Scenario

try:
    import weave
    WEAVE_AVAILABLE = True
except ImportError:
    WEAVE_AVAILABLE = False


@dataclass
class EvaluationResult:
    """Results from LLM evaluation"""
    conversation_id: str
    scenario_id: str
    model_name: str
    
    # Core evaluation scores (0-10)
    task_completion: float
    empathy: float
    clarity: float
    cultural_fit: float
    problem_solving: float
    
    # Overall score
    overall_score: float
    
    # Qualitative feedback
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[str]
    
    # Success criteria met
    success_criteria_met: Dict[str, bool]
    must_not_do_violations: List[str]
    
    # Raw LLM response
    raw_evaluation: str
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return asdict(self)
    
    def get_summary(self) -> str:
        """Get a human-readable summary"""
        return f"""
Evaluation Summary
==================
Conversation: {self.conversation_id}
Scenario: {self.scenario_id}
Model: {self.model_name}

Scores (0-10):
- Task Completion: {self.task_completion:.1f}
- Empathy: {self.empathy:.1f}
- Clarity: {self.clarity:.1f}
- Cultural Fit: {self.cultural_fit:.1f}
- Problem Solving: {self.problem_solving:.1f}
- Overall: {self.overall_score:.1f}

Strengths:
{chr(10).join(f'  ✓ {s}' for s in self.strengths)}

Weaknesses:
{chr(10).join(f'  ✗ {w}' for w in self.weaknesses)}

Recommendations:
{chr(10).join(f'  → {r}' for r in self.recommendations)}
"""


class LLMJudge:
    """LLM-based evaluator for conversation quality"""
    
    def __init__(self, judge_model: BaseModel, language: str = "arabic"):
        """
        Initialize LLM Judge
        
        Args:
            judge_model: LLM model to use for evaluation
            language: Language for evaluation prompts (arabic or english)
        """
        self.judge_model = judge_model
        self.language = language
    
    def _build_evaluation_prompt(
        self,
        scenario: Scenario,
        conversation_turns: List[Dict],
        conversation_metadata: Dict
    ) -> str:
        """Build the evaluation prompt for the judge LLM"""
        
        if self.language == "arabic":
            return self._build_arabic_prompt(scenario, conversation_turns, conversation_metadata)
        else:
            return self._build_english_prompt(scenario, conversation_turns, conversation_metadata)
    
    def _build_english_prompt(
        self,
        scenario: Scenario,
        conversation_turns: List[Dict],
        conversation_metadata: Dict
    ) -> str:
        """Build English evaluation prompt"""
        
        # Format conversation
        conversation_text = ""
        for i, turn in enumerate(conversation_turns, 1):
            conversation_text += f"\n[Turn {i}]\n"
            conversation_text += f"Customer: {turn.get('customer_message', turn.get('user_message', 'N/A'))}\n"
            conversation_text += f"Agent: {turn.get('agent_message', turn.get('assistant_message', 'N/A'))}\n"
        
        # Format success criteria
        success_criteria_text = "\n".join(f"  - {criterion}" for criterion in scenario.success_criteria)
        
        # Format must-not-do
        must_not_do_text = "\n".join(f"  - {item}" for item in scenario.must_not_do)
        
        # Format evaluation dimensions
        dimensions_text = "\n".join(
            f"  - {name}: {desc}" 
            for name, desc in scenario.evaluation_dimensions.items()
        )
        
        prompt = f"""You are an expert evaluator for Arabic customer service conversations. Your task is to evaluate the following conversation based on multiple quality dimensions.

# SCENARIO CONTEXT
**Scenario ID:** {scenario.scenario_id}
**Title:** {scenario.title}
**Description:** {scenario.description}
**Complexity:** {scenario.complexity}

**Customer Persona:**
- Name: {scenario.customer_persona.name}
- Personality: {scenario.customer_persona.personality_traits}
- Communication Style: {scenario.customer_persona.communication_style}

**Customer Goal:** {scenario.customer_goal}

# CONVERSATION
{conversation_text}

# EVALUATION CRITERIA

## Success Criteria (Must be met):
{success_criteria_text}

## Must NOT Do (Violations are serious):
{must_not_do_text}

## Evaluation Dimensions:
{dimensions_text}

# YOUR TASK
Evaluate this conversation and provide:

1. **Scores (0-10)** for each dimension:
   - task_completion: Did the agent complete the task successfully?
   - empathy: Did the agent show appropriate empathy?
   - clarity: Was communication clear and understandable?
   - cultural_fit: Did the agent use culturally appropriate language and references?
   - problem_solving: Did the agent solve the problem effectively?

2. **Success Criteria Met:** For each success criterion, indicate if it was met (yes/no)

3. **Must-Not-Do Violations:** List any violations of the "must not do" items

4. **Qualitative Feedback:**
   - Strengths (2-3 key positive points)
   - Weaknesses (2-3 key areas for improvement)
   - Recommendations (2-3 specific actionable suggestions)

5. **Overall Score (0-10):** Weighted average considering all dimensions

# OUTPUT FORMAT
Provide your evaluation in the following JSON format:

```json
{{
  "scores": {{
    "task_completion": 8.5,
    "empathy": 7.0,
    "clarity": 9.0,
    "cultural_fit": 8.0,
    "problem_solving": 7.5
  }},
  "success_criteria_met": {{
    "criterion_1": true,
    "criterion_2": false,
    ...
  }},
  "must_not_do_violations": ["violation 1", "violation 2"],
  "strengths": ["strength 1", "strength 2", "strength 3"],
  "weaknesses": ["weakness 1", "weakness 2"],
  "recommendations": ["recommendation 1", "recommendation 2"],
  "overall_score": 8.0,
  "reasoning": "Brief explanation of the overall assessment"
}}
```

Provide only the JSON, no additional text."""
        
        return prompt
    
    def _build_arabic_prompt(
        self,
        scenario: Scenario,
        conversation_turns: List[Dict],
        conversation_metadata: Dict
    ) -> str:
        """Build Arabic evaluation prompt"""
        
        # Format conversation
        conversation_text = ""
        for i, turn in enumerate(conversation_turns, 1):
            conversation_text += f"\n[الدورة {i}]\n"
            conversation_text += f"العميل: {turn.get('customer_message', turn.get('user_message', 'غير متوفر'))}\n"
            conversation_text += f"الموظف: {turn.get('agent_message', turn.get('assistant_message', 'غير متوفر'))}\n"
        
        # Format success criteria
        success_criteria_text = "\n".join(f"  - {criterion}" for criterion in scenario.success_criteria)
        
        # Format must-not-do
        must_not_do_text = "\n".join(f"  - {item}" for item in scenario.must_not_do)
        
        # Format evaluation dimensions
        dimensions_text = "\n".join(
            f"  - {name}: {desc}" 
            for name, desc in scenario.evaluation_dimensions.items()
        )
        
        prompt = f"""أنت خبير في تقييم محادثات خدمة العملاء بالعربية. مهمتك تقييم المحادثة التالية بناءً على عدة أبعاد للجودة.

# سياق السيناريو
**معرف السيناريو:** {scenario.scenario_id}
**العنوان:** {scenario.title}
**الوصف:** {scenario.description}
**مستوى التعقيد:** {scenario.complexity}

**شخصية العميل:**
- الاسم: {scenario.customer_persona.name}
- الشخصية: {scenario.customer_persona.personality_traits}
- أسلوب التواصل: {scenario.customer_persona.communication_style}

**هدف العميل:** {scenario.customer_goal}

# المحادثة
{conversation_text}

# معايير التقييم

## معايير النجاح (يجب تحقيقها):
{success_criteria_text}

## ممنوع القيام به (أي انتهاك خطير):
{must_not_do_text}

## أبعاد التقييم:
{dimensions_text}

# مهمتك
قيّم هذه المحادثة وقدم:

1. **درجات (من 0-10)** لكل بُعد:
   - task_completion: هل أكمل الموظف المهمة بنجاح؟
   - empathy: هل أظهر الموظف تعاطف مناسب؟
   - clarity: هل كان التواصل واضح ومفهوم؟
   - cultural_fit: هل استخدم الموظف لغة وتعبيرات مناسبة ثقافياً؟
   - problem_solving: هل حل الموظف المشكلة بفعالية؟

2. **تحقيق معايير النجاح:** لكل معيار، حدد إذا تم تحقيقه (نعم/لا)

3. **انتهاكات الممنوع:** اذكر أي انتهاكات لبنود "ممنوع القيام به"

4. **تقييم نوعي:**
   - نقاط القوة (2-3 نقاط إيجابية رئيسية)
   - نقاط الضعف (2-3 مجالات للتحسين)
   - التوصيات (2-3 اقتراحات محددة قابلة للتنفيذ)

5. **الدرجة الإجمالية (من 0-10):** متوسط مرجح يأخذ في الاعتبار جميع الأبعاد

# صيغة الإخراج
قدم تقييمك بصيغة JSON التالية:

```json
{{
  "scores": {{
    "task_completion": 8.5,
    "empathy": 7.0,
    "clarity": 9.0,
    "cultural_fit": 8.0,
    "problem_solving": 7.5
  }},
  "success_criteria_met": {{
    "معيار_1": true,
    "معيار_2": false,
    ...
  }},
  "must_not_do_violations": ["انتهاك 1", "انتهاك 2"],
  "strengths": ["نقطة قوة 1", "نقطة قوة 2", "نقطة قوة 3"],
  "weaknesses": ["نقطة ضعف 1", "نقطة ضعف 2"],
  "recommendations": ["توصية 1", "توصية 2"],
  "overall_score": 8.0,
  "reasoning": "شرح مختصر للتقييم الإجمالي"
}}
```

قدم JSON فقط، بدون نص إضافي."""
        
        return prompt
    
    @weave.op() if WEAVE_AVAILABLE else lambda f: f
    def evaluate_conversation(
        self,
        conversation_id: str,
        scenario: Scenario,
        conversation_turns: List[Dict],
        conversation_metadata: Dict,
        model_name: str
    ) -> EvaluationResult:
        """
        Evaluate a conversation using the judge LLM
        
        Args:
            conversation_id: Unique conversation identifier
            scenario: The test scenario
            conversation_turns: List of conversation turns
            conversation_metadata: Metadata about the conversation
            model_name: Name of the model being evaluated
            
        Returns:
            EvaluationResult with scores and feedback
        """
        
        # Build evaluation prompt
        eval_prompt = self._build_evaluation_prompt(
            scenario, 
            conversation_turns, 
            conversation_metadata
        )
        
        # Get LLM evaluation
        try:
            response = self.judge_model.generate_response(
                system_prompt="You are an expert evaluator. Provide structured JSON evaluations.",
                conversation_history=[],
                user_message=eval_prompt,
                temperature=0.3,  # Lower temperature for more consistent evaluations
                max_tokens=2048
            )
            
            raw_response = response["response"]
            
            # Extract JSON from response (handle markdown code blocks)
            json_text = raw_response
            if "```json" in json_text:
                json_text = json_text.split("```json")[1].split("```")[0].strip()
            elif "```" in json_text:
                json_text = json_text.split("```")[1].split("```")[0].strip()
            
            # Parse JSON
            evaluation_data = json.loads(json_text)
            
            # Extract scores
            scores = evaluation_data.get("scores", {})
            
            # Create evaluation result
            result = EvaluationResult(
                conversation_id=conversation_id,
                scenario_id=scenario.scenario_id,
                model_name=model_name,
                task_completion=float(scores.get("task_completion", 0)),
                empathy=float(scores.get("empathy", 0)),
                clarity=float(scores.get("clarity", 0)),
                cultural_fit=float(scores.get("cultural_fit", 0)),
                problem_solving=float(scores.get("problem_solving", 0)),
                overall_score=float(evaluation_data.get("overall_score", 0)),
                strengths=evaluation_data.get("strengths", []),
                weaknesses=evaluation_data.get("weaknesses", []),
                recommendations=evaluation_data.get("recommendations", []),
                success_criteria_met=evaluation_data.get("success_criteria_met", {}),
                must_not_do_violations=evaluation_data.get("must_not_do_violations", []),
                raw_evaluation=raw_response
            )
            
            return result
            
        except json.JSONDecodeError as e:
            # Fallback: create a result with error information
            print(f"⚠️  Failed to parse LLM evaluation JSON: {e}")
            return EvaluationResult(
                conversation_id=conversation_id,
                scenario_id=scenario.scenario_id,
                model_name=model_name,
                task_completion=0.0,
                empathy=0.0,
                clarity=0.0,
                cultural_fit=0.0,
                problem_solving=0.0,
                overall_score=0.0,
                strengths=[],
                weaknesses=["Failed to evaluate - JSON parsing error"],
                recommendations=[],
                success_criteria_met={},
                must_not_do_violations=[],
                raw_evaluation=response.get("response", "Error")
            )
        
        except Exception as e:
            print(f"⚠️  Error during evaluation: {e}")
            return EvaluationResult(
                conversation_id=conversation_id,
                scenario_id=scenario.scenario_id,
                model_name=model_name,
                task_completion=0.0,
                empathy=0.0,
                clarity=0.0,
                cultural_fit=0.0,
                problem_solving=0.0,
                overall_score=0.0,
                strengths=[],
                weaknesses=[f"Evaluation error: {str(e)}"],
                recommendations=[],
                success_criteria_met={},
                must_not_do_violations=[],
                raw_evaluation=str(e)
            )
    
    def batch_evaluate(
        self,
        conversations: List[Dict],
        scenarios: Dict[str, Scenario]
    ) -> List[EvaluationResult]:
        """
        Evaluate multiple conversations
        
        Args:
            conversations: List of conversation dictionaries
            scenarios: Dictionary mapping scenario_id to Scenario objects
            
        Returns:
            List of EvaluationResults
        """
        
        results = []
        total = len(conversations)
        
        for i, conv in enumerate(conversations, 1):
            print(f"Evaluating conversation {i}/{total}: {conv.get('conversation_id', 'unknown')}")
            
            scenario_id = conv.get("scenario_id")
            scenario = scenarios.get(scenario_id)
            
            if not scenario:
                print(f"  ⚠️  Scenario not found: {scenario_id}")
                continue
            
            try:
                result = self.evaluate_conversation(
                    conversation_id=conv.get("conversation_id", "unknown"),
                    scenario=scenario,
                    conversation_turns=conv.get("turns", []),
                    conversation_metadata=conv,
                    model_name=conv.get("model_name", "unknown")
                )
                
                results.append(result)
                print(f"  ✅ Overall Score: {result.overall_score:.1f}/10")
                
            except Exception as e:
                print(f"  ❌ Failed: {e}")
        
        return results

