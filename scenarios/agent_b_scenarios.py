"""
Agent B (Telecom) Test Scenarios - Arabic
10 scenarios with diverse customer personas for Egyptian telecom customer service
"""

from typing import List
from .scenario_loader import Scenario
from simulator.customer_simulator import CustomerPersona


def get_agent_b_scenarios() -> List[Scenario]:
    """Get all Agent B (Telecom) test scenarios"""
    
    scenarios = [
        # Scenario B1: Internet speed issue
        Scenario(
            scenario_id="B1_slow_internet",
            agent_type="agent_b_telecom",
            title="النت بطيء جداً - مهندس يشتغل من البيت",
            description="مشترك يشتكي من بطء الإنترنت وهو محتاجه للشغل",
            complexity="medium",
            customer_persona=CustomerPersona(
                name="كريم",
                age=32,
                occupation="مهندس برمجة",
                personality_traits="صبور في البداية، بس بيزعل لو الحل اتأخر",
                communication_style="تقني، بيحب يفهم المشكلة بالتفصيل",
                cultural_context="بيشتغل remote، النت مهم جداً ليه"
            ),
            customer_goal="حل مشكلة بطء الإنترنت فوراً أو معرفة متى هيترصلح",
            initial_context={
                "phone_number": "01012345678",
                "plan": "باقة 100 ميجا",
                "issue_duration": "3 أيام",
                "speed_expected": "100 ميجا",
                "speed_actual": "10 ميجا"
            },
            success_criteria=[
                "تم تشخيص سبب البطء",
                "تم تقديم حل فوري أو موعد محدد للحل",
                "تم التأكد من السرعة بعد الحل"
            ],
            evaluation_dimensions={
                "technical_competence": "هل الموظف فاهم المشكلة التقنية؟",
                "problem_solving": "هل تم تقديم حلول عملية؟",
                "empathy": "هل أظهر تفهم لتأثير المشكلة على شغل العميل؟",
                "follow_up": "هل تم الاتفاق على متابعة؟"
            },
            expected_actions=[
                "check_internet_speed",
                "troubleshoot_connection",
                "schedule_technician_visit"
            ],
            must_not_do=[
                "تجاهل الشكوى",
                "إعطاء حلول غير عملية",
                "عدم المتابعة"
            ],
            max_turns=8,
            min_turns=4
        ),
        
        # Scenario B2: High bill complaint
        Scenario(
            scenario_id="B2_high_bill",
            agent_type="agent_b_telecom",
            title="فاتورة عالية جداً - أم بيت مندهشة",
            description="عميلة فاتورتها أعلى من المعتاد بكتير",
            complexity="medium",
            customer_persona=CustomerPersona(
                name="سميرة",
                age=45,
                occupation="ربة منزل",
                personality_traits="قلقانة على الفلوس، مش فاهمة المصطلحات التقنية كويس",
                communication_style="بسيط، محتاجة شرح واضح",
                cultural_context="بتحاسب على كل قرش، خايفة الفاتورة تزيد تاني"
            ),
            customer_goal="فهم سبب ارتفاع الفاتورة وتجنب ده في المستقبل",
            initial_context={
                "phone_number": "01098765432",
                "usual_bill": "100 جنيه",
                "current_bill": "380 جنيه",
                "month": "نوفمبر"
            },
            success_criteria=[
                "تم شرح الفاتورة بالتفصيل",
                "العميلة فهمت سبب الزيادة",
                "تم تقديم نصايح لتجنب الزيادة مستقبلاً"
            ],
            evaluation_dimensions={
                "clarity": "هل الشرح كان واضح ومبسط؟",
                "patience": "هل الموظف كان صبور في الشرح؟",
                "helpfulness": "هل قدم نصايح عملية؟",
                "transparency": "هل كان واضح وصادق في الشرح؟"
            },
            expected_actions=[
                "explain_bill_details",
                "identify_extra_charges",
                "suggest_appropriate_package"
            ],
            must_not_do=[
                "استخدام مصطلحات معقدة",
                "التسرع في الشرح",
                "تجاهل قلق العميلة"
            ],
            max_turns=7,
            min_turns=4
        ),
        
        # Scenario B3: SIM card activation issue
        Scenario(
            scenario_id="B3_sim_activation",
            agent_type="agent_b_telecom",
            title="شريحة جديدة مش شغالة - شاب محتاج رقمه فوراً",
            description="عميل اشترى شريحة جديدة ومش شغالة",
            complexity="simple",
            customer_persona=CustomerPersona(
                name="محمد",
                age=22,
                occupation="طالب جامعي",
                personality_traits="مستعجل، محتاج يتصل بشكل عاجل",
                communication_style="مباشر، عايز حل سريع",
                cultural_context="محتاج الرقم لإنترفيو شغل"
            ),
            customer_goal="تشغيل الشريحة الجديدة فوراً",
            initial_context={
                "new_number": "01155555555",
                "purchase_date": "اليوم الصبح",
                "issue": "الشريحة بتقول No Service"
            },
            success_criteria=[
                "تم تفعيل الشريحة بنجاح",
                "العميل قدر يتصل",
                "تم التأكد من عمل الخدمة"
            ],
            evaluation_dimensions={
                "speed": "هل تم الحل بسرعة؟",
                "effectiveness": "هل الحل نجح؟",
                "communication": "هل تم توجيه العميل بوضوح؟"
            },
            expected_actions=[
                "verify_sim_activation",
                "guide_manual_activation",
                "test_service"
            ],
            must_not_do=[
                "التأخير في الحل",
                "إعطاء خطوات معقدة",
                "عدم التأكد من الحل"
            ],
            max_turns=5,
            min_turns=2
        ),
        
        # Scenario B4: Package upgrade request
        Scenario(
            scenario_id="B4_package_upgrade",
            agent_type="agent_b_telecom",
            title="ترقية الباقة - موظف محتاج نت أكتر",
            description="عميل عايز يغير باقته لباقة أعلى",
            complexity="simple",
            customer_persona=CustomerPersona(
                name="أحمد",
                age=28,
                occupation="موظف مبيعات",
                personality_traits="واضح، عارف هو عايز إيه",
                communication_style="مباشر ومحترم",
                cultural_context="بيستخدم النت كتير للشغل والتواصل"
            ),
            customer_goal="ترقية الباقة لباقة أعلى ومعرفة التكلفة",
            initial_context={
                "phone_number": "01123456789",
                "current_plan": "باقة 50 ميجا",
                "desired_plan": "باقة 200 ميجا"
            },
            success_criteria=[
                "تم شرح خيارات الترقية",
                "تم توضيح الأسعار والمزايا",
                "تم تنفيذ الترقية أو حجزها"
            ],
            evaluation_dimensions={
                "information_quality": "هل تم توضيح كل التفاصيل؟",
                "sales_approach": "هل كان البيع محترم ومش ضاغط؟",
                "efficiency": "هل تمت العملية بسلاسة؟"
            },
            expected_actions=[
                "check_available_packages",
                "explain_pricing",
                "process_upgrade"
            ],
            must_not_do=[
                "الضغط لبيع باقات أغلى",
                "إخفاء تفاصيل التكلفة",
                "التسرع بدون شرح"
            ],
            max_turns=6,
            min_turns=3
        ),
        
        # Scenario B5: Network coverage complaint
        Scenario(
            scenario_id="B5_no_coverage",
            agent_type="agent_b_telecom",
            title="مفيش شبكة في منطقته - ساكن في منطقة جديدة",
            description="عميل بيشتكي من ضعف التغطية في منطقته",
            complexity="high",
            customer_persona=CustomerPersona(
                name="مصطفى",
                age=35,
                occupation="دكتور",
                personality_traits="محترم بس متضايق، محتاج حل جدي",
                communication_style="راقي، بيشرح المشكلة بالتفصيل",
                cultural_context="انتقل لمنطقة جديدة، الشبكة ضعيفة جداً"
            ),
            customer_goal="حل مشكلة التغطية أو البحث عن بدائل",
            initial_context={
                "phone_number": "01098765432",
                "area": "الشيخ زايد - منطقة جديدة",
                "issue_duration": "أسبوع",
                "signal_strength": "ضعيف جداً أو مفيش"
            },
            success_criteria=[
                "تم التحقق من التغطية في المنطقة",
                "تم تقديم حلول واقعية",
                "تم التصعيد إن لزم الأمر"
            ],
            evaluation_dimensions={
                "honesty": "هل كان صادق عن وضع التغطية؟",
                "problem_solving": "هل قدم حلول بديلة؟",
                "escalation": "هل صعد المشكلة للمسؤول؟"
            },
            expected_actions=[
                "check_coverage_map",
                "report_weak_coverage",
                "suggest_alternatives",
                "escalate_to_technical_team"
            ],
            must_not_do=[
                "إنكار المشكلة",
                "إعطاء وعود كاذبة",
                "تجاهل الشكوى"
            ],
            max_turns=8,
            min_turns=4
        ),
        
        # Scenario B6: International roaming confusion
        Scenario(
            scenario_id="B6_roaming_confusion",
            agent_type="agent_b_telecom",
            title="مسافر برة مصر وخايف من الفاتورة",
            description="عميل مسافر ومش فاهم خدمة التجوال الدولي",
            complexity="medium",
            customer_persona=CustomerPersona(
                name="نادية",
                age=38,
                occupation="مديرة تسويق",
                personality_traits="منظمة، بتخطط قبل السفر",
                communication_style="واضحة، بتسأل أسئلة محددة",
                cultural_context="مسافرة للسعودية لمدة أسبوع، خايفة من فاتورة كبيرة"
            ),
            customer_goal="فهم خيارات التجوال وتفعيل الأنسب قبل السفر",
            initial_context={
                "phone_number": "01234567890",
                "destination": "السعودية",
                "duration": "أسبوع",
                "travel_date": "بعد 3 أيام"
            },
            success_criteria=[
                "تم شرح خيارات التجوال الدولي",
                "تم توضيح الأسعار بوضوح",
                "تم تفعيل الباقة المناسبة"
            ],
            evaluation_dimensions={
                "clarity": "هل الشرح كان واضح ومفهوم؟",
                "transparency": "هل تم توضيح كل التكاليف؟",
                "customer_focus": "هل تم اختيار الأنسب للعميلة؟"
            },
            expected_actions=[
                "explain_roaming_options",
                "calculate_costs",
                "activate_roaming_package"
            ],
            must_not_do=[
                "إخفاء تكاليف مخفية",
                "بيع باقة أغلى بدون داعي",
                "الشرح بشكل معقد"
            ],
            max_turns=7,
            min_turns=4
        ),
        
        # Scenario B7: Lost/stolen phone
        Scenario(
            scenario_id="B7_lost_phone",
            agent_type="agent_b_telecom",
            title="موبايله اتسرق - قلقان على رقمه وبياناته",
            description="عميل موبايله اتسرق وعايز يوقف الخط",
            complexity="high",
            customer_persona=CustomerPersona(
                name="ياسر",
                age=29,
                occupation="محاسب",
                personality_traits="متوتر ومستعجل، خايف على بياناته",
                communication_style="سريع، قلقان",
                cultural_context="موبايله فيه حسابات بنكية ومعلومات مهمة"
            ),
            customer_goal="وقف الخط فوراً وحماية بياناته",
            initial_context={
                "phone_number": "01012345678",
                "incident": "السرقة حصلت من ساعة",
                "has_backup": "مفيش backup للرقم"
            },
            success_criteria=[
                "تم وقف الخط فوراً",
                "تم شرح خطوات استعادة الرقم",
                "تم طمأنة العميل"
            ],
            evaluation_dimensions={
                "urgency_response": "هل تم التعامل بسرعة مناسبة؟",
                "security_focus": "هل تم التركيز على الأمان؟",
                "empathy": "هل أظهر تعاطف مع موقف العميل؟",
                "guidance": "هل تم توجيه العميل للخطوات التالية؟"
            },
            expected_actions=[
                "block_line_immediately",
                "verify_identity",
                "explain_number_recovery",
                "suggest_police_report"
            ],
            must_not_do=[
                "التأخير في وقف الخط",
                "طلب إجراءات معقدة قبل الوقف",
                "عدم التعاطف مع الموقف"
            ],
            max_turns=6,
            min_turns=3
        ),
        
        # Scenario B8: Contract cancellation
        Scenario(
            scenario_id="B8_cancel_contract",
            agent_type="agent_b_telecom",
            title="عايز يلغي الخط - مسافر برة مصر نهائي",
            description="عميل مسافر بشكل دائم وعايز يلغي العقد",
            complexity="medium",
            customer_persona=CustomerPersona(
                name="عمر",
                age=26,
                occupation="مهندس",
                personality_traits="حاسم، عارف هو عايز إيه",
                communication_style="واضح ومباشر",
                cultural_context="مسافر كندا للعمل، مش هيرجع مصر قريب"
            ),
            customer_goal="إلغاء الخط وتسوية أي مستحقات",
            initial_context={
                "phone_number": "01123456789",
                "contract_duration": "سنتين",
                "remaining_months": "4 شهور",
                "travel_date": "الأسبوع الجاي"
            },
            success_criteria=[
                "تم شرح شروط الإلغاء",
                "تم حساب المستحقات",
                "تم بدء إجراءات الإلغاء"
            ],
            evaluation_dimensions={
                "transparency": "هل تم شرح كل التكاليف بوضوح؟",
                "professionalism": "هل حاول الاحتفاظ بالعميل بشكل محترم؟",
                "efficiency": "هل تمت العملية بسلاسة؟"
            },
            expected_actions=[
                "explain_cancellation_terms",
                "calculate_early_termination_fee",
                "process_cancellation"
            ],
            must_not_do=[
                "إخفاء تكاليف الإلغاء",
                "الضغط بشكل غير مريح",
                "تعقيد الإجراءات"
            ],
            max_turns=7,
            min_turns=4
        ),
        
        # Scenario B9: Data package not working
        Scenario(
            scenario_id="B9_data_not_working",
            agent_type="agent_b_telecom",
            title="باقة النت اشتراها ومش شغالة - طالبة محتاجة النت للامتحانات",
            description="عميلة اشترت باقة نت ومش شغالة",
            complexity="simple",
            customer_persona=CustomerPersona(
                name="سلمى",
                age=20,
                occupation="طالبة جامعية",
                personality_traits="قلقانة، عندها امتحان أونلاين",
                communication_style="مهذبة بس قلقانة",
                cultural_context="محتاجة النت للامتحان بعد ساعتين"
            ),
            customer_goal="تشغيل باقة النت فوراً",
            initial_context={
                "phone_number": "01098765432",
                "package_purchased": "باقة 5 جيجا",
                "purchase_time": "من ساعة",
                "issue": "النت مش شغال خالص"
            },
            success_criteria=[
                "تم حل المشكلة فوراً",
                "النت اشتغل",
                "تم التأكد من عمل الباقة"
            ],
            evaluation_dimensions={
                "urgency_handling": "هل تعامل مع الاستعجال بجدية؟",
                "problem_solving": "هل تم حل المشكلة بسرعة؟",
                "empathy": "هل أظهر تفهم لموقف الطالبة؟"
            },
            expected_actions=[
                "check_package_activation",
                "activate_data_service",
                "verify_internet_working"
            ],
            must_not_do=[
                "التأخير في الحل",
                "تجاهل استعجال العميلة",
                "إعطاء حلول معقدة"
            ],
            max_turns=5,
            min_turns=2
        ),
        
        # Scenario B10: Elderly customer - basic inquiry
        Scenario(
            scenario_id="B10_elderly_inquiry",
            agent_type="agent_b_telecom",
            title="عميل كبير في السن - استفسار عن الرصيد",
            description="عميل كبير في السن عايز يعرف رصيده",
            complexity="simple",
            customer_persona=CustomerPersona(
                name="حاج عبد الله",
                age=68,
                occupation="متقاعد",
                personality_traits="طيب، بطيء في الفهم، محتاج صبر",
                communication_style="بسيط جداً، بيحب الشرح المفصل",
                cultural_context="مش متعود على التكنولوجيا كتير"
            ),
            customer_goal="معرفة رصيده وإزاي يشحن",
            initial_context={
                "phone_number": "01012345678",
                "issue": "عايز يعرف رصيده",
                "secondary_need": "عايز يعرف إزاي يشحن"
            },
            success_criteria=[
                "تم إخباره بالرصيد",
                "تم شرح طريقة الشحن بوضوح",
                "العميل فهم كل حاجة"
            ],
            evaluation_dimensions={
                "patience": "هل كان صبور مع العميل؟",
                "clarity": "هل الشرح كان بسيط وواضح؟",
                "respect": "هل تعامل باحترام مع كبير السن؟",
                "repetition_tolerance": "هل كان مستعد يعيد الشرح؟"
            },
            expected_actions=[
                "check_balance",
                "explain_recharge_methods",
                "repeat_instructions_slowly"
            ],
            must_not_do=[
                "الاستعجال",
                "استخدام مصطلحات معقدة",
                "عدم الصبر"
            ],
            max_turns=8,
            min_turns=4
        )
    ]
    
    return scenarios
