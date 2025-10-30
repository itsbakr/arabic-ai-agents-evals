"""
Agent A (E-commerce) Test Scenarios - Arabic
10 scenarios with diverse customer personas
"""

from typing import List
from .scenario_loader import Scenario
from simulator.customer_simulator import CustomerPersona


def get_agent_a_scenarios() -> List[Scenario]:
    """Get all Agent A (E-commerce) test scenarios"""
    
    scenarios = []
    
    # ============================================================================
    # Scenario A1: Late Delivery - Impatient Young Professional
    # ============================================================================
    scenarios.append(Scenario(
        scenario_id="A1_late_delivery",
        agent_type="agent_a",
        title="تأخير التوصيل - موظف شاب مستعجل",
        description="عميل طلب موبايل من 10 أيام ولم يصل، لديه اجتماع مهم",
        complexity="medium",
        
        customer_persona=CustomerPersona(
            name="أحمد",
            age=28,
            personality="مستعجل وقلق، محتاج الموبايل بشكل عاجل للشغل",
            communication_style="مباشر، يستخدم اللهجة المصرية",
            patience_level=4,
            tech_literacy="high",
            cultural_context="urban_cairo",
            language_style="egyptian_dialect"
        ),
        
        customer_goal="معرفة حالة الطلب ومتى سيصل الموبايل بالضبط، محتاجه لاجتماع مهم",
        
        initial_context={
            "رقم الطلب": "EG45891",
            "المنتج": "موبايل Samsung Galaxy S23",
            "تاريخ الطلب": "منذ 10 أيام",
            "المدينة": "الجيزة",
            "السعر": "18,500 جنيه - دفع عند الاستلام"
        },
        
        success_criteria=[
            "العميل عرف حالة طلبه",
            "حصل على موعد محدد للتوصيل",
            "الموظف أظهر تعاطف مع استعجاله",
            "تم اتخاذ إجراء لتسريع التوصيل أو التصعيد"
        ],
        
        evaluation_dimensions={
            "task_completion": "هل تم التحقق من حالة الطلب وإعطاء معلومات دقيقة؟",
            "empathy": "هل أظهر الموظف تعاطف مع استعجال العميل؟",
            "proactivity": "هل قدم حلول استباقية (تسريع، تعويض، الخ)؟",
            "clarity": "هل كانت المعلومات واضحة ومحددة؟",
            "cultural_fit": "هل استخدم أسلوب مناسب للثقافة المصرية؟"
        },
        
        expected_actions=[
            "check_order_status(EG45891)",
            "تقديم اعتذار واضح",
            "إعطاء موعد محدد للتوصيل",
            "عرض تعويض أو تصعيد إذا طلب العميل"
        ],
        
        must_not_do=[
            "تجاهل استعجال العميل",
            "إعطاء مواعيد غير واقعية",
            "عدم التحقق من حالة الطلب"
        ],
        
        max_turns=8,
        min_turns=3
    ))
    
    # ============================================================================
    # Scenario A2: Wrong Item Delivered - Frustrated Bride-to-be
    # ============================================================================
    scenarios.append(Scenario(
        scenario_id="A2_wrong_item",
        agent_type="agent_a",
        title="منتج غلط - عروسة محتاجة فستان للفرح",
        description="عروسة طلبت فستان أزرق ووصلها قميص أحمر، الفرح بعد يومين",
        complexity="high",
        
        customer_persona=CustomerPersona(
            name="منى",
            age=26,
            personality="زعلانة جداً ومتوترة، خايفة الفستان مايجيش قبل الفرح",
            communication_style="عاطفي، تستخدم اللهجة المصرية، تعبر عن قلقها بوضوح",
            patience_level=2,
            tech_literacy="medium",
            cultural_context="urban_cairo",
            language_style="egyptian_dialect"
        ),
        
        customer_goal="استرجاع المنتج الغلط والحصول على الفستان الصح قبل الفرح بأي طريقة",
        
        initial_context={
            "رقم الطلب": "EG67234",
            "المنتج المطلوب": "فستان أزرق مقاس M",
            "المنتج الواصل": "قميص أحمر مقاس L",
            "تاريخ الفرح": "بعد يومين (يوم الجمعة)",
            "السعر": "2,500 جنيه - دفع عند الاستلام"
        },
        
        success_criteria=[
            "الموظف أظهر تعاطف كبير مع موقف الفرح",
            "تم بدء عملية إرجاع فوراً",
            "تم عرض حل سريع (توصيل عاجل، استرداد، الخ)",
            "العميلة اطمأنت أو حصلت على حل بديل",
            "تم التصعيد للمشرف إذا لزم الأمر"
        ],
        
        evaluation_dimensions={
            "emotional_intelligence": "هل تعامل مع الحالة النفسية للعميلة بحساسية؟",
            "urgency_handling": "هل فهم أهمية الموقف (فرح) وتصرف بسرعة؟",
            "solution_quality": "هل الحل المقترح واقعي ومناسب للوقت المتبقي؟",
            "empathy": "هل أظهر تعاطف حقيقي مع موقف الفرح؟",
            "cultural_sensitivity": "هل فهم أهمية الفرح في الثقافة المصرية؟"
        },
        
        expected_actions=[
            "process_return(EG67234, 'wrong_item')",
            "اعتذار قوي وصادق",
            "عرض توصيل عاجل للفستان الصحيح",
            "escalate_to_supervisor للحصول على موافقة سريعة",
            "تقديم تعويض (خصم، شحن مجاني، الخ)"
        ],
        
        must_not_do=[
            "التقليل من أهمية الموقف",
            "إعطاء مواعيد غير واقعية (بعد الفرح)",
            "عدم التصعيد رغم الاستعجال الشديد"
        ],
        
        max_turns=10,
        min_turns=4
    ))
    
    # ============================================================================
    # Scenario A3: Ramadan Delivery Timing - Family Man Planning Eid
    # ============================================================================
    scenarios.append(Scenario(
        scenario_id="A3_ramadan_timing",
        agent_type="agent_a",
        title="توقيت التوصيل في رمضان - أب يحضر للعيد",
        description="أب عايز يطلب هدايا العيد لأولاده، قلقان من التأخير في رمضان",
        complexity="medium",
        
        customer_persona=CustomerPersona(
            name="محمود",
            age=42,
            personality="مسؤول وحريص، عايز يفرح أولاده في العيد",
            communication_style="محترم، يستخدم 'حضرتك'، لهجة مصرية متزنة",
            patience_level=7,
            tech_literacy="medium",
            cultural_context="religious",
            language_style="egyptian_dialect"
        ),
        
        customer_goal="الاطمئنان أن الطلب هيوصل قبل العيد، ومعرفة الوقت المناسب للطلب",
        
        initial_context={
            "التوقيت": "رمضان، باقي 12 يوم على العيد",
            "المنتجات": "ألعاب وملابس أطفال (3 أطفال)",
            "القيمة المتوقعة": "3,500 جنيه",
            "المدينة": "المنصورة",
            "طريقة الدفع": "دفع عند الاستلام"
        },
        
        success_criteria=[
            "الموظف شرح تأثير رمضان على التوصيل بوضوح",
            "أعطى موعد توصيل واقعي",
            "نصح العميل بالطلب مبكراً",
            "أظهر فهم لأهمية العيد للأطفال",
            "أكد على إمكانية الدفع عند الاستلام"
        ],
        
        evaluation_dimensions={
            "cultural_awareness": "هل فهم سياق رمضان والعيد؟",
            "transparency": "هل كان صريح عن التأخيرات المحتملة؟",
            "helpfulness": "هل قدم نصائح مفيدة؟",
            "respect": "هل أظهر احترام للسياق الديني؟",
            "clarity": "هل المعلومات واضحة ومحددة؟"
        },
        
        expected_actions=[
            "شرح سياسة التوصيل في رمضان (+2-3 أيام)",
            "نصح بالطلب على الأقل 10 أيام قبل العيد",
            "تأكيد توفر المنتجات",
            "تأكيد إمكانية الدفع عند الاستلام"
        ],
        
        must_not_do=[
            "عدم ذكر تأخيرات رمضان",
            "إعطاء وعود غير واقعية",
            "التجاهل أهمية العيد"
        ],
        
        max_turns=7,
        min_turns=3
    ))
    
    # ============================================================================
    # Scenario A4: Expensive Laptop Refund - Tech-Savvy Student
    # ============================================================================
    scenarios.append(Scenario(
        scenario_id="A4_laptop_refund",
        agent_type="agent_a",
        title="استرداد مبلغ لابتوب معطل - طالب جامعي",
        description="طالب جامعي اشترى لابتوب غالي ومعطل، عايز فلوسه يرجع مش بديل",
        complexity="high",
        
        customer_persona=CustomerPersona(
            name="عمر",
            age=21,
            personality="واثق من حقه، فاهم تقنياً، مصر على الاسترداد مش البديل",
            communication_style="مباشر، يستخدم مصطلحات تقنية، لهجة مصرية",
            patience_level=5,
            tech_literacy="high",
            cultural_context="urban_cairo",
            language_style="egyptian_dialect"
        ),
        
        customer_goal="استرداد كامل المبلغ المدفوع، مش عايز بديل لأنه فقد الثقة",
        
        initial_context={
            "رقم الطلب": "EG88542",
            "المنتج": "Laptop Dell XPS 15",
            "المشكلة": "الشاشة بترمش (Hardware issue)",
            "السعر المدفوع": "32,000 جنيه بالبطاقة",
            "تاريخ الاستلام": "منذ 5 أيام",
            "الفترة المتبقية للإرجاع": "9 أيام"
        },
        
        success_criteria=[
            "تم بدء عملية الإرجاع",
            "تم تأكيد الاسترداد الكامل",
            "شرح واضح للجدول الزمني (5-7 أيام عمل)",
            "ترتيب استلام اللابتوب المعطل",
            "إعطاء رقم متابعة للحالة"
        ],
        
        evaluation_dimensions={
            "process_clarity": "هل شرح عملية الإرجاع والاسترداد بوضوح؟",
            "professionalism": "هل تعامل باحترافية مع طلب الاسترداد؟",
            "timeline_accuracy": "هل أعطى جدول زمني دقيق؟",
            "customer_rights": "هل احترم حق العميل في الإرجاع؟",
            "follow_up": "هل قدم طريقة لمتابعة الحالة؟"
        },
        
        expected_actions=[
            "process_return(EG88542, 'defective')",
            "issue_refund(EG88542, 32000, 'card')",
            "شرح مدة الاسترداد (5-7 أيام عمل)",
            "ترتيب استلام المنتج",
            "إعطاء رقم حالة Case number"
        ],
        
        must_not_do=[
            "محاولة إقناعه بالبديل رغم رفضه",
            "إعطاء مدة استرداد غير صحيحة",
            "عدم ترتيب استلام المنتج المعطل"
        ],
        
        max_turns=8,
        min_turns=4
    ))
    
    # ============================================================================
    # Scenario A5: Address Change After Shipment - Recent Mover
    # ============================================================================
    scenarios.append(Scenario(
        scenario_id="A5_address_change",
        agent_type="agent_a",
        title="تغيير العنوان بعد الشحن - منتقل لشقة جديدة",
        description="عميلة انتقلت لشقة جديدة والطلب اتشحن على العنوان القديم",
        complexity="high",
        
        customer_persona=CustomerPersona(
            name="نورهان",
            age=30,
            personality="قلقانة ومتوترة من الموقف، مش عارفة تعمل إيه",
            communication_style="سريع، قلقان، لهجة مصرية",
            patience_level=4,
            tech_literacy="medium",
            cultural_context="urban_cairo",
            language_style="egyptian_dialect"
        ),
        
        customer_goal="تغيير عنوان التوصيل للشقة الجديدة أو إيجاد حل بديل",
        
        initial_context={
            "رقم الطلب": "EG33421",
            "المنتج": "أجهزة منزلية (خلاط، مكواة)",
            "العنوان القديم": "المعادي",
            "العنوان الجديد": "التجمع الخامس",
            "حالة الشحن": "في الطريق للتوصيل",
            "السعر": "1,200 جنيه - دفع عند الاستلام"
        },
        
        success_criteria=[
            "الموظف شرح أنه لا يمكن تغيير العنوان بعد الشحن (Policy)",
            "قدم حلول بديلة واقعية",
            "أظهر تعاطف مع موقف الانتقال",
            "العميل فهم الخيارات المتاحة",
            "تم الوصول لحل يرضي العميل"
        ],
        
        evaluation_dimensions={
            "policy_communication": "هل شرح السياسة بوضوح ولطف؟",
            "problem_solving": "هل قدم حلول بديلة عملية؟",
            "empathy": "هل أظهر تعاطف مع موقف الانتقال؟",
            "alternatives": "كم حل بديل قدم؟",
            "customer_satisfaction": "هل العميل قبل بحل من الحلول؟"
        },
        
        expected_actions=[
            "check_order_status(EG33421)",
            "شرح سياسة عدم تغيير العنوان بعد الشحن",
            "تقديم بدائل: (1) رفض الاستلام وإعادة الشحن، (2) شخص يستلم من العنوان القديم، (3) التواصل مع السائق",
            "محاولة التواصل مع فريق التوصيل"
        ],
        
        must_not_do=[
            "رفض مساعدة العميل بدون بدائل",
            "عدم شرح السياسة بوضوح",
            "ترك العميل بدون حل"
        ],
        
        max_turns=10,
        min_turns=4
    ))
    
    # ============================================================================
    # Scenario A6: COD Payment Limit - Large Order Concern
    # ============================================================================
    scenarios.append(Scenario(
        scenario_id="A6_cod_large_order",
        agent_type="agent_a",
        title="طلب كبير بالدفع عند الاستلام - قلق من الحد الأقصى",
        description="عميل عايز يطلب أجهزة كهربائية بقيمة 15,000 جنيه ومش واثق في الدفع الإلكتروني",
        complexity="medium",
        
        customer_persona=CustomerPersona(
            name="سمير",
            age=50,
            personality="حذر، مش واثق في الدفع الإلكتروني، يفضل الكاش",
            communication_style="متأني، يسأل أسئلة كتير، لهجة مصرية",
            patience_level=8,
            tech_literacy="low",
            cultural_context="traditional",
            language_style="egyptian_dialect"
        ),
        
        customer_goal="الاطمئنان أنه يقدر يطلب ويدفع كاش عند الاستلام، وفهم الضمانات",
        
        initial_context={
            "المنتجات المطلوبة": "ثلاجة + غسالة",
            "القيمة التقديرية": "15,000 جنيه",
            "طريقة الدفع المفضلة": "دفع عند الاستلام (COD)",
            "المدينة": "طنطا",
            "القلق الرئيسي": "عدم الثقة في الدفع الإلكتروني"
        },
        
        success_criteria=[
            "الموظف طمأن العميل أن COD متاح للطلبات الكبيرة",
            "شرح إجراءات الأمان والفحص قبل الدفع",
            "أعطى معلومات عن الضمان والإرجاع",
            "أظهر احترام لتفضيل العميل للكاش",
            "ساعد في إتمام الطلب"
        ],
        
        evaluation_dimensions={
            "reassurance": "هل طمأن العميل بخصوص مخاوفه؟",
            "clarity": "هل شرح العملية بوضوح لشخص tech literacy منخفض؟",
            "respect": "هل احترم تفضيل العميل للدفع الكاش؟",
            "completeness": "هل أعطى كل المعلومات اللازمة؟",
            "cultural_fit": "هل فهم ثقافة الكاش في مصر؟"
        },
        
        expected_actions=[
            "تأكيد توفر COD للطلبات الكبيرة",
            "شرح إجراءات الفحص قبل الدفع",
            "شرح سياسة الإرجاع والضمان",
            "تأكيد مدة التوصيل لمدينته"
        ],
        
        must_not_do=[
            "محاولة إجباره على الدفع الإلكتروني",
            "التقليل من مخاوفه",
            "استخدام مصطلحات تقنية معقدة"
        ],
        
        max_turns=9,
        min_turns=4
    ))
    
    # ============================================================================
    # Scenario A7: Damaged Product on Delivery - Angry Customer
    # ============================================================================
    scenarios.append(Scenario(
        scenario_id="A7_damaged_delivery",
        agent_type="agent_a",
        title="منتج وصل مكسور - عميل غاضب جداً",
        description="عميل استلم تليفزيون مكسور والسائق مشي، زعلان جداً",
        complexity="high",
        
        customer_persona=CustomerPersona(
            name="كريم",
            age=35,
            personality="غضبان جداً، محبط، حاسس إنه اتظلم",
            communication_style="عصبي، صوته عالي، لهجة مصرية قوية",
            patience_level=2,
            tech_literacy="medium",
            cultural_context="urban_cairo",
            language_style="egyptian_dialect"
        ),
        
        customer_goal="استرجاع فلوسه فوراً أو استبدال التليفزيون المكسور بواحد جديد",
        
        initial_context={
            "رقم الطلب": "EG77889",
            "المنتج": "تليفزيون Samsung 55 بوصة",
            "المشكلة": "وصل مكسور (الشاشة متشققة)",
            "السعر": "12,000 جنيه - دفع عند الاستلام (دفع بالفعل)",
            "وقت الاستلام": "منذ ساعتين",
            "ملاحظة": "السائق رفض يستنى والعميل كان مستعجل فدفع"
        },
        
        success_criteria=[
            "الموظف امتص غضب العميل بتعاطف",
            "اعتذار قوي وفوري",
            "اتخاذ إجراء فوري (إرجاع + استبدال أو استرداد)",
            "تصعيد للمشرف لضمان حل سريع",
            "العميل هدى وحس أنه هيتحل مشكلته"
        ],
        
        evaluation_dimensions={
            "de_escalation": "هل نجح في تهدئة العميل الغاضب؟",
            "accountability": "هل اعترف بالخطأ بوضوح؟",
            "action_speed": "هل اتخذ إجراء فوري؟",
            "empathy": "هل أظهر تعاطف حقيقي مع الموقف؟",
            "resolution_quality": "هل الحل المقترح عادل وسريع؟"
        },
        
        expected_actions=[
            "اعتذار قوي وفوري",
            "process_return(EG77889, 'damaged')",
            "عرض استبدال فوري + تعويض",
            "escalate_to_supervisor لحل عاجل",
            "ترتيب استلام التليفزيون المكسور"
        ],
        
        must_not_do=[
            "لوم العميل أو السائق",
            "طلب صور أو إجراءات معقدة بدون حل فوري",
            "عدم الاعتراف بالخطأ",
            "إعطاء وعود غير واقعية"
        ],
        
        max_turns=10,
        min_turns=5
    ))
    
    # ============================================================================
    # Scenario A8: Elderly Customer - Simple Inquiry
    # ============================================================================
    scenarios.append(Scenario(
        scenario_id="A8_elderly_simple",
        agent_type="agent_a",
        title="عميلة كبيرة في السن - استفسار بسيط",
        description="سيدة كبيرة في السن عايزة تطلب هدية لحفيدها ومحتاجة مساعدة",
        complexity="simple",
        
        customer_persona=CustomerPersona(
            name="حاجة فاطمة",
            age=68,
            personality="طيبة وصبورة، لكن مش فاهمة كويس التكنولوجيا",
            communication_style="محترم جداً، بطيء، يحتاج شرح مفصل",
            patience_level=9,
            tech_literacy="low",
            cultural_context="traditional",
            language_style="egyptian_dialect"
        ),
        
        customer_goal="طلب لعبة لحفيدها وفهم كيفية الطلب والدفع والاستلام",
        
        initial_context={
            "المنتج المطلوب": "لعبة سيارة كهربائية للأطفال",
            "السعر التقريبي": "500 جنيه",
            "المدينة": "الإسكندرية",
            "الخبرة بالتسوق الإلكتروني": "أول مرة",
            "القلق الرئيسي": "عدم فهم الخطوات"
        },
        
        success_criteria=[
            "الموظف كان صبور جداً",
            "شرح كل خطوة ببساطة شديدة",
            "استخدم أسلوب محترم (حاجة، حضرتك)",
            "طمأن العميلة على الإجراءات",
            "ساعدها في إتمام الطلب خطوة بخطوة"
        ],
        
        evaluation_dimensions={
            "patience": "هل كان صبور مع كبار السن؟",
            "simplicity": "هل استخدم لغة بسيطة وواضحة؟",
            "respect": "هل أظهر احترام كبير لكبار السن؟",
            "step_by_step": "هل شرح كل خطوة بالتفصيل؟",
            "cultural_sensitivity": "هل استخدم أسلوب مناسب لكبار السن المصريين؟"
        },
        
        expected_actions=[
            "شرح خطوات الطلب ببساطة",
            "تأكيد أن الدفع عند الاستلام متاح",
            "شرح مدة التوصيل بوضوح",
            "طمأنتها على الإجراءات"
        ],
        
        must_not_do=[
            "استخدام مصطلحات تقنية معقدة",
            "الاستعجال أو إظهار ملل",
            "عدم شرح الخطوات بالتفصيل"
        ],
        
        max_turns=12,
        min_turns=5
    ))
    
    # ============================================================================
    # Scenario A9: Promotional Discount Confusion
    # ============================================================================
    scenarios.append(Scenario(
        scenario_id="A9_promo_confusion",
        agent_type="agent_a",
        title="خلط في العروض والخصومات",
        description="عميل شاف إعلان خصم 30% لكن السعر في الموقع مختلف",
        complexity="medium",
        
        customer_persona=CustomerPersona(
            name="هشام",
            age=33,
            personality="محبط ومتشكك، حاسس إنه في خداع في الإعلان",
            communication_style="متشكك، يطلب أدلة، لهجة مصرية",
            patience_level=5,
            tech_literacy="high",
            cultural_context="urban_cairo",
            language_style="egyptian_dialect"
        ),
        
        customer_goal="فهم الخصم وهل ينطبق على المنتج اللي عايزه، أو الحصول على تعويض",
        
        initial_context={
            "المنتج": "سماعات AirPods Pro",
            "السعر الأصلي": "6,500 جنيه",
            "السعر المعروض": "6,200 جنيه",
            "الخصم المتوقع (30%)": "4,550 جنيه",
            "الإعلان": "شاف إعلان على فيسبوك بخصم 30%",
            "الكود الترويجي": "SALE30"
        },
        
        success_criteria=[
            "الموظف شرح شروط العرض بوضوح",
            "أوضح الفرق بين السعر والتوقعات",
            "قدم بدائل أو حلول (كود مختلف، منتجات أخرى)",
            "حافظ على مصداقية الشركة",
            "العميل فهم الموقف"
        ],
        
        evaluation_dimensions={
            "transparency": "هل كان شفاف عن شروط العروض؟",
            "problem_solving": "هل قدم حلول بديلة؟",
            "credibility": "هل حافظ على مصداقية الشركة؟",
            "clarity": "هل أوضح سبب الخلط؟",
            "customer_satisfaction": "هل العميل اقتنع بالشرح؟"
        },
        
        expected_actions=[
            "شرح شروط العرض (يمكن العرض على فئة معينة)",
            "التحقق من الكود الترويجي",
            "عرض خصومات أو أكواد بديلة",
            "شرح السعر الحالي (ممكن فيه خصم أقل)"
        ],
        
        must_not_do=[
            "إنكار وجود العرض",
            "لوم العميل على سوء الفهم",
            "عدم تقديم حل أو بديل"
        ],
        
        max_turns=8,
        min_turns=4
    ))
    
    # ============================================================================
    # Scenario A10: Multiple Orders Confusion
    # ============================================================================
    scenarios.append(Scenario(
        scenario_id="A10_multiple_orders",
        agent_type="agent_a",
        title="خلط بين أكثر من طلب",
        description="عميلة عندها 3 طلبات ومش فاهمة أيهم وصل وأيهم لسه",
        complexity="medium",
        
        customer_persona=CustomerPersona(
            name="دينا",
            age=38,
            personality="مشوشة ومحتاجة توضيح، مش متأكدة من أرقام الطلبات",
            communication_style="سريع، مشوش شوية، لهجة مصرية",
            patience_level=6,
            tech_literacy="medium",
            cultural_context="urban_cairo",
            language_style="egyptian_dialect"
        ),
        
        customer_goal="فهم حالة كل طلب، ومعرفة أيهم وصل وأيهم لسه",
        
        initial_context={
            "الطلب 1": "EG11223 - فستان (وصل)",
            "الطلب 2": "EG11224 - أحذية (في الطريق)",
            "الطلب 3": "EG11225 - شنطة (لم يشحن بعد)",
            "الخلط": "العميلة مش متأكدة أي طلب وصل",
            "المدينة": "القاهرة"
        },
        
        success_criteria=[
            "الموظف فحص كل الطلبات بنظام",
            "أوضح حالة كل طلب بشكل منفصل",
            "استخدم أسلوب منظم (Tracking لكل طلب)",
            "طمأن العميلة وأزال الشوشرة",
            "أعطى مواعيد واضحة للطلبات المتبقية"
        ],
        
        evaluation_dimensions={
            "organization": "هل رتب المعلومات بشكل واضح؟",
            "clarity": "هل أوضح كل طلب على حدة؟",
            "patience": "هل كان صبور مع الشوشرة؟",
            "reassurance": "هل طمأن العميلة؟",
            "completeness": "هل أعطى معلومات كاملة عن كل الطلبات؟"
        },
        
        expected_actions=[
            "check_order_status(EG11223)",
            "check_order_status(EG11224)",
            "check_order_status(EG11225)",
            "توضيح حالة كل طلب منفصلة",
            "إعطاء مواعيد متوقعة للطلبات المتبقية"
        ],
        
        must_not_do=[
            "الخلط بين الطلبات",
            "إعطاء معلومات مبهمة",
            "عدم فحص كل الطلبات"
        ],
        
        max_turns=9,
        min_turns=4
    ))
    
    return scenarios

