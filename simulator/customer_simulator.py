"""
Customer simulator for realistic LLM-to-LLM interactions
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from models.base_model import BaseModel

try:
    import weave
    WEAVE_AVAILABLE = True
except ImportError:
    WEAVE_AVAILABLE = False


@dataclass
class CustomerPersona:
    """
    Customer persona for simulation
    """
    name: str
    age: int
    personality: str  # frustrated, polite, confused, angry, urgent, elderly, tech_savvy, etc.
    communication_style: str  # formal, casual, dialect-heavy, etc.
    patience_level: int  # 1-10 (1 = very impatient, 10 = very patient)
    tech_literacy: str  # low, medium, high
    cultural_context: str  # urban_cairo, rural, religious, etc.
    language_style: str  # egyptian_dialect, msa (modern standard arabic), mixed
    
    def to_prompt_description(self) -> str:
        """Convert persona to natural language description"""
        return f"""أنت تلعب دور {self.name}، عميل/عميلة مصري/ة عمرك {self.age} سنة.

الشخصية والأسلوب:
- الحالة النفسية: {self.personality}
- أسلوب التواصل: {self.communication_style}
- مستوى الصبر: {self.patience_level}/10
- الإلمام بالتكنولوجيا: {self.tech_literacy}
- السياق الثقافي: {self.cultural_context}
- اللغة المستخدمة: {self.language_style}

تعليمات مهمة:
- تصرف بشكل طبيعي كعميل مصري حقيقي
- استخدم اللهجة المصرية بشكل طبيعي
- أظهر المشاعر المناسبة للموقف
- كن واقعياً في ردود فعلك
- لا تكون متعاوناً بشكل مبالغ فيه - تصرف كعميل حقيقي
- إذا كان الموظف غير واضح أو غير مفيد، عبر عن عدم رضاك
- إذا حل الموظف مشكلتك بشكل جيد، اشكره بصدق
"""


class CustomerSimulator:
    """
    Simulates customer behavior in conversations
    """
    
    def __init__(self, model: BaseModel, language: str = "arabic"):
        """
        Initialize customer simulator
        
        Args:
            model: LLM model to use for simulation
            language: Language for simulation
        """
        self.model = model
        self.language = language
        self.conversation_history: List[Dict[str, str]] = []
        
    @weave.op() if WEAVE_AVAILABLE else lambda f: f
    def generate_response(
        self,
        persona: CustomerPersona,
        goal: str,
        context: Dict[str, any],
        agent_message: str,
        turn_number: int,
        max_turns: int = 10
    ) -> Dict[str, any]:
        """
        Generate customer response based on persona and goal
        
        Args:
            persona: Customer persona
            goal: Customer's goal in the conversation
            context: Additional context (order numbers, account info, etc.)
            agent_message: Latest message from agent
            turn_number: Current turn number
            max_turns: Maximum number of turns
            
        Returns:
            Dictionary with response and metadata
        """
        
        # Build system prompt for customer
        system_prompt = self._build_customer_prompt(
            persona, goal, context, turn_number, max_turns
        )
        
        # Add agent's message to history
        if agent_message:
            self.conversation_history.append({
                "role": "user",
                "content": f"[رسالة من موظف خدمة العملاء]: {agent_message}"
            })
        
        # Generate customer response
        result = self.model.generate_response(
            system_prompt=system_prompt,
            conversation_history=self.conversation_history,
            user_message="[قم بالرد على موظف خدمة العملاء بناءً على دورك كعميل]",
            temperature=0.8,  # Higher temperature for more natural variation
            max_tokens=300
        )
        
        if result["response"]:
            # Add customer's response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": result["response"]
            })
            
            # Check if customer wants to end conversation
            should_end = self._should_end_conversation(
                result["response"], turn_number, max_turns
            )
            
            return {
                "response": result["response"],
                "should_end": should_end,
                "turn_number": turn_number,
                "tokens_used": result["tokens_used"],
                "error": result["error"]
            }
        else:
            return {
                "response": None,
                "should_end": True,
                "turn_number": turn_number,
                "tokens_used": 0,
                "error": result["error"]
            }
    
    @weave.op() if WEAVE_AVAILABLE else lambda f: f
    def generate_initial_message(
        self,
        persona: CustomerPersona,
        goal: str,
        context: Dict[str, any]
    ) -> str:
        """
        Generate the initial customer message to start conversation
        
        Args:
            persona: Customer persona
            goal: Customer's goal
            context: Additional context
            
        Returns:
            Initial customer message
        """
        system_prompt = f"""{persona.to_prompt_description()}

هدفك من المحادثة:
{goal}

معلومات إضافية:
{self._format_context(context)}

تعليمات:
- ابدأ المحادثة بشكل طبيعي كعميل مصري
- اذكر المشكلة أو الطلب بوضوح
- استخدم اللهجة المصرية
- أظهر المشاعر المناسبة للموقف
- اجعل رسالتك قصيرة ومباشرة (2-4 جمل)
"""
        
        result = self.model.generate_response(
            system_prompt=system_prompt,
            conversation_history=[],
            user_message="ابدأ المحادثة مع خدمة العملاء الآن:",
            temperature=0.8,
            max_tokens=200
        )
        
        if result["response"]:
            return result["response"].strip()
        else:
            # Fallback to context-based message
            return self._generate_fallback_message(goal, context)
    
    def _build_customer_prompt(
        self,
        persona: CustomerPersona,
        goal: str,
        context: Dict[str, any],
        turn_number: int,
        max_turns: int
    ) -> str:
        """Build system prompt for customer simulator"""
        
        prompt = f"""{persona.to_prompt_description()}

هدفك من المحادثة:
{goal}

معلومات إضافية لديك:
{self._format_context(context)}

أنت الآن في المحادثة (الدورة {turn_number} من {max_turns}):

إرشادات للرد:
1. رد بشكل طبيعي على ما قاله الموظف
2. إذا طلب منك معلومات لديك، قدمها
3. إذا لم يحل المشكلة، اسأل عن الخطوات التالية
4. إذا كان الموظف غير واضح، اطلب توضيح
5. إذا حُلّت المشكلة، اشكره وأنهِ المحادثة
6. إذا لم يكن متعاوناً، عبّر عن إحباطك
7. استخدم اللهجة المصرية بشكل طبيعي

تذكر:
- أنت عميل حقيقي، ليس متعاوناً بشكل مبالغ
- أظهر مشاعرك الحقيقية
- كن واقعياً في ردود فعلك
- إذا وصلت لهدفك، أنهِ المحادثة بشكل طبيعي
"""
        
        return prompt
    
    def _format_context(self, context: Dict[str, any]) -> str:
        """Format context dictionary as readable text"""
        if not context:
            return "لا توجد معلومات إضافية"
        
        formatted = []
        for key, value in context.items():
            formatted.append(f"- {key}: {value}")
        return "\n".join(formatted)
    
    def _should_end_conversation(
        self,
        customer_response: str,
        turn_number: int,
        max_turns: int
    ) -> bool:
        """
        Determine if customer wants to end conversation
        
        Args:
            customer_response: Customer's latest response
            turn_number: Current turn number
            max_turns: Maximum turns allowed
            
        Returns:
            True if conversation should end
        """
        # Check for thank you and goodbye phrases
        end_phrases = [
            "شكرا", "شكراً", "ربنا يباركلك", "تمام كده",
            "خلاص", "ماشي", "مع السلامة", "الله يكرمك",
            "تسلم", "يعطيك العافية", "ممتاز"
        ]
        
        response_lower = customer_response.lower()
        
        # Check if response contains ending phrases
        contains_thanks = any(phrase in response_lower for phrase in end_phrases)
        
        # Check if response is very short (likely ending)
        is_short = len(customer_response.split()) < 10
        
        # End if max turns reached
        if turn_number >= max_turns:
            return True
        
        # End if customer seems satisfied
        if contains_thanks and is_short:
            return True
        
        return False
    
    def _generate_fallback_message(self, goal: str, context: Dict[str, any]) -> str:
        """Generate fallback message if LLM fails"""
        return f"السلام عليكم، {goal}"
    
    def reset(self):
        """Reset conversation history"""
        self.conversation_history = []

