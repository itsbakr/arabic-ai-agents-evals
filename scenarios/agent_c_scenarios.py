"""
Agent C (Banking) Test Scenarios - Arabic
10 scenarios with diverse customer personas for Egyptian banking customer service
"""

from typing import List
from .scenario_loader import Scenario
from simulator.customer_simulator import CustomerPersona


def get_agent_c_scenarios() -> List[Scenario]:
    """Get all Agent C (Banking) test scenarios"""
    
    scenarios = [
        # Scenario C1: Lost/Stolen card
        Scenario(
            scenario_id="C1_stolen_card",
            agent_type="agent_c_banking",
            title="كارت الفيزا اتسرق - قلقان على فلوسه",
            description="عميل كارته اتسرق وعايز يوقفه فوراً",
            complexity="high",
            customer_persona=CustomerPersona(
                name="محمود",
                age=34,
                occupation="مهندس",
                personality_traits="متوتر جداً، خايف على فلوسه",
                communication_style="سريع ومباشر، محتاج حل فوري",
                cultural_context="فيه معاملات غريبة حصلت على الكارت"
            ),
            customer_goal="وقف الكارت فوراً ومنع أي معاملات غير مصرح بها",
            initial_context={
                "account_number": "1234567890",
                "card_last_4": "5678",
                "incident": "السرقة حصلت من ساعتين",
                "suspicious_transactions": "في معاملتين مش عارفهم"
            },
            success_criteria=[
                "تم وقف الكارت فوراً",
                "تم التحقق من المعاملات المشبوهة",
                "تم شرح خطوات إصدار كارت جديد",
                "تم طمأنة العميل"
            ],
            evaluation_dimensions={
                "urgency_response": "هل تم التعامل بالسرعة المطلوبة؟",
                "security_focus": "هل تم التأكيد على الأمان؟",
                "empathy": "هل أظهر تعاطف مع قلق العميل؟",
                "clarity": "هل تم شرح الإجراءات بوضوح؟"
            },
            expected_actions=[
                "block_card_immediately",
                "verify_identity",
                "investigate_suspicious_transactions",
                "explain_new_card_process"
            ],
            must_not_do=[
                "التأخير في وقف الكارت",
                "طلب إجراءات معقدة قبل الوقف",
                "عدم التحقق من المعاملات المشبوهة"
            ],
            max_turns=8,
            min_turns=4
        ),
        
        # Scenario C2: Unable to access online banking
        Scenario(
            scenario_id="C2_online_banking_locked",
            agent_type="agent_c_banking",
            title="مش قادر يدخل على النت بانكينج - نسي الباسورد",
            description="عميل محتاج يدخل حسابه أونلاين ومش قادر",
            complexity="simple",
            customer_persona=CustomerPersona(
                name="هدى",
                age=28,
                occupation="محامية",
                personality_traits="منظمة بس مستعجلة",
                communication_style="واضحة ومباشرة",
                cultural_context="محتاجة تحول فلوس فوراً"
            ),
            customer_goal="استعادة الوصول للحساب الإلكتروني",
            initial_context={
                "account_number": "9876543210",
                "issue": "نسيت الباسورد وجربت 3 مرات",
                "account_status": "مقفول"
            },
            success_criteria=[
                "تم التحقق من الهوية",
                "تم إعادة تعيين الباسورد",
                "العميلة قدرت تدخل حسابها"
            ],
            evaluation_dimensions={
                "security_compliance": "هل تم التحقق من الهوية بشكل صحيح؟",
                "efficiency": "هل تم الحل بسرعة؟",
                "guidance": "هل تم توجيه العميلة بوضوح؟"
            },
            expected_actions=[
                "verify_identity_thoroughly",
                "reset_password",
                "unlock_account"
            ],
            must_not_do=[
                "التساهل في التحقق من الهوية",
                "إعطاء معلومات حساسة بدون تحقق",
                "تعقيد الإجراءات بدون داعي"
            ],
            max_turns=6,
            min_turns=3
        ),
        
        # Scenario C3: Loan inquiry
        Scenario(
            scenario_id="C3_loan_inquiry",
            agent_type="agent_c_banking",
            title="استفسار عن قرض شخصي - موظف عايز يشتري عربية",
            description="عميل عايز يعرف عن القروض الشخصية",
            complexity="medium",
            customer_persona=CustomerPersona(
                name="عمرو",
                age=30,
                occupation="محاسب",
                personality_traits="حذر مالياً، عايز يفهم كل التفاصيل",
                communication_style="بيسأل أسئلة كتير، دقيق",
                cultural_context="أول مرة ياخد قرض، شوية خايف"
            ),
            customer_goal="فهم شروط القرض والفوائد والأقساط",
            initial_context={
                "account_age": "5 سنوات",
                "monthly_salary": "10000 جنيه",
                "desired_amount": "150000 جنيه",
                "purpose": "شراء سيارة"
            },
            success_criteria=[
                "تم شرح أنواع القروض المتاحة",
                "تم توضيح الفوائد والأقساط",
                "تم شرح الشروط والمستندات",
                "العميل قرر الخطوة التالية"
            ],
            evaluation_dimensions={
                "information_quality": "هل تم تقديم معلومات كاملة ودقيقة؟",
                "transparency": "هل تم توضيح كل التكاليف؟",
                "patience": "هل كان صبور مع أسئلة العميل؟",
                "sales_ethics": "هل كان البيع أخلاقي بدون ضغط؟"
            },
            expected_actions=[
                "explain_loan_types",
                "calculate_monthly_payments",
                "list_required_documents",
                "check_eligibility"
            ],
            must_not_do=[
                "إخفاء تكاليف مخفية",
                "الضغط لقبول القرض",
                "إعطاء معلومات غير دقيقة"
            ],
            max_turns=10,
            min_turns=5
        ),
        
        # Scenario C4: Transaction dispute
        Scenario(
            scenario_id="C4_transaction_dispute",
            agent_type="agent_c_banking",
            title="معاملة مش عارفها - اتخصمت من حسابه",
            description="عميل في معاملة على حسابه مش عارفها",
            complexity="high",
            customer_persona=CustomerPersona(
                name="نورهان",
                age=35,
                occupation="دكتورة",
                personality_traits="قلقانة، عايزة تفهم إيه اللي حصل",
                communication_style="هادية بس مصرة على حل المشكلة",
                cultural_context="بتراجع حسابها بانتظام"
            ),
            customer_goal="معرفة تفاصيل المعاملة وإلغاءها إن كانت خطأ",
            initial_context={
                "account_number": "5555666677",
                "transaction_amount": "2500 جنيه",
                "transaction_date": "إمبارح",
                "merchant": "متجر أونلاين مش عارفاه"
            },
            success_criteria=[
                "تم التحقق من تفاصيل المعاملة",
                "تم فتح بلاغ dispute",
                "تم شرح خطوات التحقيق",
                "تم تحديد timeline للحل"
            ],
            evaluation_dimensions={
                "investigation_quality": "هل تم التحقيق بدقة؟",
                "communication": "هل تم شرح الإجراءات بوضوح؟",
                "empathy": "هل أظهر تفهم لقلق العميلة؟",
                "follow_up": "هل تم وضع خطة للمتابعة؟"
            },
            expected_actions=[
                "investigate_transaction_details",
                "file_dispute_claim",
                "explain_investigation_process",
                "set_follow_up_timeline"
            ],
            must_not_do=[
                "رفض البلاغ بدون تحقيق",
                "تجاهل قلق العميلة",
                "عدم وضع timeline واضح"
            ],
            max_turns=8,
            min_turns=4
        ),
        
        # Scenario C5: Account opening inquiry
        Scenario(
            scenario_id="C5_new_account",
            agent_type="agent_c_banking",
            title="فتح حساب جديد - خريج جديد بدأ شغل",
            description="عميل جديد عايز يفتح حساب",
            complexity="medium",
            customer_persona=CustomerPersona(
                name="مريم",
                age=23,
                occupation="خريجة حديثة - موظفة جديدة",
                personality_traits="متحمسة، مش عارفة كتير عن البنوك",
                communication_style="فضولية، بتسأل كتير",
                cultural_context="أول حساب بنكي ليها"
            ),
            customer_goal="فتح حساب مناسب لاحتياجاتها كموظفة جديدة",
            initial_context={
                "employment_status": "موظفة جديدة",
                "monthly_salary": "5000 جنيه",
                "needs": "حساب راتب + كارت فيزا"
            },
            success_criteria=[
                "تم شرح أنواع الحسابات",
                "تم اختيار الحساب المناسب",
                "تم شرح المستندات المطلوبة",
                "تم حجز موعد لفتح الحساب"
            ],
            evaluation_dimensions={
                "educational_approach": "هل تم الشرح بطريقة تعليمية؟",
                "patience": "هل كان صبور مع العميلة الجديدة؟",
                "guidance": "هل تم توجيهها للخيار الأنسب؟",
                "clarity": "هل كان الشرح واضح ومبسط؟"
            },
            expected_actions=[
                "explain_account_types",
                "recommend_suitable_account",
                "list_required_documents",
                "schedule_branch_visit"
            ],
            must_not_do=[
                "استخدام مصطلحات معقدة",
                "التسرع في الشرح",
                "بيع خدمات غير مناسبة"
            ],
            max_turns=9,
            min_turns=5
        ),
        
        # Scenario C6: ATM card swallowed
        Scenario(
            scenario_id="C6_atm_card_stuck",
            agent_type="agent_c_banking",
            title="الماكينة بلعت الكارت - محتاج فلوس فوراً",
            description="عميل كارته اتبلع في ماكينة الصراف",
            complexity="medium",
            customer_persona=CustomerPersona(
                name="خالد",
                age=40,
                occupation="تاجر",
                personality_traits="مستعجل، محتاج يسحب فلوس ضروري",
                communication_style="مباشر، شوية منفعل",
                cultural_context="محتاج فلوس لدفع فاتورة مهمة"
            ),
            customer_goal="استرجاع الكارت أو الحصول على طريقة بديلة للسحب",
            initial_context={
                "atm_location": "فرع المعادي",
                "incident_time": "قبل نص ساعة",
                "card_type": "كارت فيزا",
                "urgency": "محتاج يسحب 5000 جنيه فوراً"
            },
            success_criteria=[
                "تم تسجيل البلاغ",
                "تم تقديم حل بديل فوري",
                "تم شرح خطوات استرجاع الكارت",
                "العميل قدر يسحب الفلوس"
            ],
            evaluation_dimensions={
                "urgency_handling": "هل تعامل مع الاستعجال بجدية؟",
                "problem_solving": "هل قدم حلول بديلة؟",
                "empathy": "هل أظهر تفهم للموقف؟",
                "efficiency": "هل تم الحل بسرعة؟"
            },
            expected_actions=[
                "log_atm_incident",
                "provide_immediate_withdrawal_solution",
                "explain_card_recovery_process",
                "issue_temporary_card_or_code"
            ],
            must_not_do=[
                "تجاهل الاستعجال",
                "عدم تقديم حلول بديلة",
                "التأخير في الحل"
            ],
            max_turns=7,
            min_turns=4
        ),
        
        # Scenario C7: Savings account interest inquiry
        Scenario(
            scenario_id="C7_savings_interest",
            agent_type="agent_c_banking",
            title="عايز يوفر فلوس - مدرس بيخطط للمستقبل",
            description="عميل عايز يفتح حساب توفير ويعرف الفوائد",
            complexity="simple",
            customer_persona=CustomerPersona(
                name="أحمد",
                age=45,
                occupation="مدرس",
                personality_traits="حريص على المال، بيخطط للمستقبل",
                communication_style="هادي، محتاج معلومات واضحة",
                cultural_context="عايز يوفر لتعليم أولاده"
            ),
            customer_goal="فهم خيارات التوفير واختيار الأنسب",
            initial_context={
                "existing_account": "حساب جاري",
                "amount_to_save": "50000 جنيه",
                "goal": "توفير لتعليم الأولاد",
                "timeline": "5 سنوات"
            },
            success_criteria=[
                "تم شرح خيارات التوفير المختلفة",
                "تم توضيح نسب الفائدة",
                "تم اختيار الخيار الأنسب",
                "تم شرح شروط السحب"
            ],
            evaluation_dimensions={
                "information_quality": "هل تم تقديم معلومات كاملة ودقيقة؟",
                "financial_advice": "هل تم تقديم نصيحة مالية مناسبة؟",
                "clarity": "هل كان الشرح واضح؟",
                "customer_focus": "هل تم التركيز على احتياج العميل؟"
            },
            expected_actions=[
                "explain_savings_options",
                "compare_interest_rates",
                "recommend_suitable_product",
                "explain_withdrawal_conditions"
            ],
            must_not_do=[
                "بيع منتج غير مناسب",
                "إخفاء شروط مهمة",
                "التسرع بدون شرح كامل"
            ],
            max_turns=8,
            min_turns=4
        ),
        
        # Scenario C8: International transfer
        Scenario(
            scenario_id="C8_international_transfer",
            agent_type="agent_c_banking",
            title="تحويل فلوس برة مصر - أم بتبعت فلوس لابنها",
            description="عميلة عايزة تحول فلوس لابنها بره مصر",
            complexity="high",
            customer_persona=CustomerPersona(
                name="فاطمة",
                age=55,
                occupation="ربة منزل",
                personality_traits="قلقانة، مش متعودة على التحويلات الدولية",
                communication_style="بسيط، محتاجة شرح مفصل",
                cultural_context="ابنها طالب في أمريكا ومحتاج فلوس"
            ),
            customer_goal="تحويل فلوس لابنها بأمان وبأقل تكلفة",
            initial_context={
                "amount": "30000 جنيه",
                "destination": "أمريكا",
                "recipient": "ابنها الطالب",
                "urgency": "محتاجها خلال يومين"
            },
            success_criteria=[
                "تم شرح خيارات التحويل الدولي",
                "تم توضيح المصاريف وسعر الصرف",
                "تم شرح المستندات المطلوبة",
                "تم إتمام التحويل أو حجزه"
            ],
            evaluation_dimensions={
                "clarity": "هل كان الشرح واضح ومبسط؟",
                "patience": "هل كان صبور مع العميلة؟",
                "transparency": "هل تم توضيح كل التكاليف؟",
                "guidance": "هل تم توجيهها خطوة بخطوة؟"
            },
            expected_actions=[
                "explain_international_transfer_options",
                "calculate_fees_and_exchange_rate",
                "list_required_documents",
                "process_transfer"
            ],
            must_not_do=[
                "استخدام مصطلحات معقدة",
                "إخفاء مصاريف",
                "التسرع في الإجراءات"
            ],
            max_turns=10,
            min_turns=5
        ),
        
        # Scenario C9: Mobile banking setup
        Scenario(
            scenario_id="C9_mobile_banking_setup",
            agent_type="agent_c_banking",
            title="عايز يفعل الموبايل بانكينج - شاب تقني",
            description="عميل عايز يفعل تطبيق البنك على موبايله",
            complexity="simple",
            customer_persona=CustomerPersona(
                name="كريم",
                age=26,
                occupation="مبرمج",
                personality_traits="تقني، سريع الفهم",
                communication_style="مباشر، عايز خطوات واضحة",
                cultural_context="بيفضل يعمل كل حاجة من الموبايل"
            ),
            customer_goal="تفعيل وتأمين حسابه على تطبيق الموبايل",
            initial_context={
                "account_number": "1234567890",
                "has_smartphone": "أيوه",
                "app_status": "مش محمله"
            },
            success_criteria=[
                "تم شرح خطوات تحميل التطبيق",
                "تم تفعيل الحساب على التطبيق",
                "تم شرح إعدادات الأمان",
                "العميل قدر يدخل حسابه"
            ],
            evaluation_dimensions={
                "clarity": "هل كانت الخطوات واضحة؟",
                "security_focus": "هل تم التأكيد على الأمان؟",
                "efficiency": "هل تم الإعداد بسرعة؟",
                "technical_accuracy": "هل المعلومات التقنية دقيقة؟"
            },
            expected_actions=[
                "guide_app_download",
                "walk_through_activation",
                "explain_security_settings",
                "verify_successful_login"
            ],
            must_not_do=[
                "إعطاء خطوات خاطئة",
                "تجاهل إعدادات الأمان",
                "التسرع بدون تأكيد الفهم"
            ],
            max_turns=6,
            min_turns=3
        ),
        
        # Scenario C10: Elderly customer - pension inquiry
        Scenario(
            scenario_id="C10_pension_inquiry",
            agent_type="agent_c_banking",
            title="عميل كبير في السن - استفسار عن المعاش",
            description="عميل متقاعد عايز يفهم تفاصيل معاشه",
            complexity="simple",
            customer_persona=CustomerPersona(
                name="حاج محمد",
                age=70,
                occupation="متقاعد",
                personality_traits="طيب، بطيء الفهم، محتاج صبر",
                communication_style="بسيط جداً، بيحتاج شرح متكرر",
                cultural_context="معاشه مصدر دخله الوحيد"
            ),
            customer_goal="فهم تفاصيل معاشه ومواعيد صرفه",
            initial_context={
                "account_number": "9999888877",
                "pension_type": "معاش تأمينات",
                "concern": "المعاش وصل أقل من المعتاد"
            },
            success_criteria=[
                "تم شرح تفاصيل المعاش",
                "تم توضيح سبب أي تغيير",
                "العميل فهم كل حاجة",
                "تم طمأنته"
            ],
            evaluation_dimensions={
                "patience": "هل كان صبور جداً مع العميل؟",
                "respect": "هل تعامل باحترام وتقدير؟",
                "clarity": "هل كان الشرح بسيط وواضح؟",
                "empathy": "هل أظهر تعاطف مع موقف العميل؟"
            },
            expected_actions=[
                "explain_pension_details_simply",
                "clarify_any_deductions",
                "reassure_customer",
                "offer_written_summary"
            ],
            must_not_do=[
                "الاستعجال",
                "استخدام مصطلحات معقدة",
                "عدم الصبر على التكرار"
            ],
            max_turns=10,
            min_turns=5
        )
    ]
    
    return scenarios
