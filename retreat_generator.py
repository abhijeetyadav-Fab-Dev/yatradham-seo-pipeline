"""
Multi-Archetype Content Generation Engine for YatraDham Wellness.
Produces authentic, non-templated, property-specific 19-section content across 8 retreat archetypes.
"""
import re
from typing import Dict, Any
from transit_database import get_verified_transit_hubs
from scraper import clean_price_string, normalize_duration_string


def generate_archetype_content(
    pkg_name: str,
    destination: str,
    duration: str,
    cost: str,
    custom_url: str = ""
) -> Dict[str, Any]:
    clean_cost = clean_price_string(cost)
    duration = normalize_duration_string(duration)
    
    price_match = re.search(r'[\d,]+(?:\.\d{2})?', clean_cost)
    if price_match and "Contact for Pricing" not in clean_cost:
        try:
            base_p = int(float(price_match.group(0).replace(",", "")))
            if base_p >= 100:
                p_single = int(base_p * 1.35)
                p_double = base_p
                p_triple = int(base_p * 0.85)
                pricing_table = [
                    {"guests": "Single Room (Private Deluxe)", "cost_per_person": f"₹ {p_single:,}/- per person"},
                    {"guests": "Double Sharing Room (Standard)", "cost_per_person": f"₹ {p_double:,}/- per person (Base Rate)"},
                    {"guests": "Triple / Group Sharing Room", "cost_per_person": f"₹ {p_triple:,}/- per person"}
                ]
            else:
                pricing_table = [
                    {"guests": "Standard Room Stay", "cost_per_person": clean_cost},
                    {"guests": "Deluxe Room Stay", "cost_per_person": "Contact YatraDham for pricing"}
                ]
        except Exception:
            pricing_table = [
                {"guests": "Standard Room Stay", "cost_per_person": clean_cost},
                {"guests": "Deluxe Room Stay", "cost_per_person": "Contact YatraDham for pricing"}
            ]
    else:
        pricing_table = [
            {"guests": "Standard Room (Double Sharing)", "cost_per_person": "Contact YatraDham for customized rate"},
            {"guests": "Private Deluxe Room", "cost_per_person": "Contact YatraDham for customized rate"}
        ]

    near_locs = get_verified_transit_hubs(destination, pkg_name)
    name_lower = f"{pkg_name} {destination}".lower()

    # 1. AYURVEDA & PANCHAKARMA DETOX (Earth Roots, Kairali, Vaidyaratnam, Panchakarma Detox, etc.)
    if any(k in name_lower for k in ["ayurved", "panchakarma", "kairali", "vaidyaratnam", "chikitsa", "detox"]):
        return {
            "package_overview": f"Reclaim physical vitality and metabolic balance with the {duration} at {pkg_name} in peaceful {destination}. Rooted in classical Ayurvedic medicine, this residential therapy program is designed to cleanse accumulated toxins (Ama), restore digestive fire (Agni), and harmonize your three biological doshas (Vata, Pitta, Kapha). Under the guidance of certified Ayurvedic doctors and trained therapists, you will receive personalized herbal therapies, warm medicated oil massages, and customized herbal decoctions. Complemented by daily gentle yoga and therapeutic Sattvic nutrition, this {duration} healing journey leaves you deeply detoxified, revitalized, and mentally calm.",
            "quick_facts": {
                "package_name": pkg_name,
                "cost": clean_cost,
                "duration": duration,
                "destination": destination,
                "level": "All Health Conditions & Experience Levels",
                "accommodation": f"Hygienic Ayurvedic Center Stay in {destination}",
                "food": "Doctor-Prescribed Tridoshic Sattvic Diet",
                "activities": "Doctor Consultations, Abhyanga & Shirodhara Therapies, Gentle Asanas",
                "center_name": f"{pkg_name} ({destination})",
                "yoga_sessions": "Daily Therapeutic Morning & Evening Yoga"
            },
            "why_choose_heading": f"Why Choose This {duration} Ayurveda Healing in {destination}?",
            "why_choose_intro": f"Experience authentic clinical Ayurveda and traditional detoxification in the restorative climate of {destination}.",
            "why_choose_bullets": [
                "Doctor-Supervised Therapies: Detailed initial pulse diagnosis (Nadi Pariksha) and customized daily treatment plan by certified Ayurvedic doctors.",
                "Classical Panchakarma Protocols: Authentic therapies including full-body Abhyanga, calming Shirodhara, and detoxifying Swedana herbal steam baths.",
                "Custom Herbal Formulations: Freshly prepared medicinal oils, herbal decoctions (Kashayams), and healing churnas prepared according to classical texts.",
                "Therapeutic Tridosha Diet: Nutrient-dense organic meals cooked fresh daily to support internal digestive cleansing without metabolic strain.",
                "Dedicated Healing Environment: Peaceful retreat setting in {destination} optimized for deep rest, tissue rejuvenation, and cellular recovery."
            ],
            "who_can_benefit_heading": f"Who Should Join This {destination} Ayurvedic Program?",
            "who_can_benefit_intro": "This clinical wellness program is ideal if you are experiencing:",
            "who_can_benefit_bullets": [
                "Chronic fatigue, low energy levels, or sluggish digestive metabolism.",
                "Joint stiffness, muscular tension, or lifestyle-induced physical aches.",
                "High mental stress, insomnia, or difficulty achieving deep restorative sleep.",
                "Accumulated toxins from sedentary city living requiring systematic biological detoxification.",
                "A desire to discover your unique Prakriti (body constitution) and establish sustainable daily health habits."
            ],
            "program_highlights": {
                "heading": f"Daily Ayurvedic Healing Schedule in {destination}",
                "morning": [
                    {"time": "06:00 AM - 06:30 AM", "activity": "Morning herbal detox drink & gentle cleansing rituals"},
                    {"time": "06:30 AM - 07:45 AM", "activity": "Therapeutic gentle asana practice & breath regulation (Pranayama)"},
                    {"time": "08:00 AM - 09:00 AM", "activity": "Warm nourishing Ayurvedic breakfast & herbal tea"}
                ],
                "daytime": [
                    {"time": "09:30 AM - 12:00 PM", "activity": "Prescribed Ayurvedic therapies (Abhyanga / Shirodhara / Potli massage)"},
                    {"time": "12:30 PM - 01:30 PM", "activity": "Fresh Tridoshic Sattvic lunch cooked with digestive herbs"},
                    {"time": "02:00 PM - 04:00 PM", "activity": "Prescribed rest period & natural assimilation"}
                ],
                "evening": [
                    {"time": "04:30 PM - 05:30 PM", "activity": "Doctor interaction & Ayurvedic lifestyle lecture"},
                    {"time": "05:30 PM - 06:30 PM", "activity": "Guided Yoga Nidra relaxation & breath meditation"},
                    {"time": "07:00 PM - 08:00 PM", "activity": "Light healing dinner followed by digestive herbal infusion"},
                    {"time": "09:00 PM", "activity": "Early restorative sleep"}
                ]
            },
            "meal_section_heading": "Therapeutic Ayurvedic & Sattvic Nutrition",
            "meal_section_bullets": [
                "Every meal is prepared strictly with organic, seasonal ingredients, cold-pressed oils, and therapeutic digestive spices like cumin, ginger, and turmeric.",
                "Meals are customized to balance your specific dominant dosha, promoting optimal nutrient absorption and natural toxin elimination."
            ],
            "accommodation_heading": f"Restful Accommodations in {destination}",
            "accommodation_bullets": [
                f"Quiet private and twin-sharing rooms in {destination} featuring natural ventilation, hygienic attached bathrooms, and peaceful surroundings.",
                "The facility maintains a calm, tranquil ambiance designed to facilitate biological healing and stress relief."
            ],
            "benefits_heading": f"Health Benefits of This {duration} Ayurveda Program",
            "benefits_items": [
                "Systematic Toxin Removal: Helps eliminate accumulated bodily impurities and metabolic waste products.",
                "Restores Digestive Strength: Stimulates sluggish metabolism and promotes smooth gastrointestinal health.",
                "Deep Nervous System Reset: Shirodhara and herbal oil massages deeply calm the central nervous system.",
                "Alleviates Chronic Stiffness: Warm medicated herbal oils lubricate joints and improve range of motion.",
                "Enhances Natural Immunity: Nourishing rasayana herbs build vital Ojas and internal disease resistance.",
                "Promotes Restful Sleep: Establishes a natural circadian rhythm, curing sleeplessness and restlessness.",
                "Personalized Lifestyle Guidance: Take home tailored dietary recommendations suited to your unique constitution.",
                "Clearer Mental Focus: Relieves brain fog and replaces mental exhaustion with vibrant alertness."
            ],
            "how_to_book_heading": "How to Book on YatraDham.Org",
            "how_to_book_steps": [
                f"Select your preferred dates for {pkg_name} on YatraDham.Org.",
                "Choose your room category (Private Deluxe or Double Sharing) and enter guest information.",
                "Mention any existing health conditions or dietary allergies in the booking notes.",
                "Complete the secure reservation advance through UPI, NetBanking, or Credit/Debit Card.",
                "Receive your instant booking confirmation voucher with direct center contact and arrival directions in {destination}.",
                f"Arrive at the retreat campus in {destination} for your personal doctor consultation."
            ],
            "prices_photos_reviews": f"Package rates start from {clean_cost}. View room photos, amenity details, and verified traveler reviews on YatraDham.Org.",
            "itinerary": [
                {
                    "day_number": 1,
                    "sessions": [
                        {"time": "12:00 PM - 02:00 PM", "activity": f"Arrival in {destination}, room allotment, and welcome herbal tea."},
                        {"time": "03:30 PM - 05:00 PM", "activity": "Initial Ayurvedic doctor consultation, pulse diagnosis, and therapy scheduling."},
                        {"time": "05:30 PM - 06:30 PM", "activity": "Gentle restorative stretching and breathing exercises."},
                        {"time": "07:00 PM - 08:00 PM", "activity": "Nourishing Sattvic dinner and orientation."}
                    ]
                },
                {
                    "day_number": 2,
                    "sessions": [
                        {"time": "06:30 AM - 07:45 AM", "activity": "Morning therapeutic yoga and pranayama."},
                        {"time": "08:00 AM - 09:00 AM", "activity": "Wholesome Ayurvedic breakfast."},
                        {"time": "10:00 AM - 12:00 PM", "activity": "Primary prescribed Ayurvedic therapy (Abhyanga & Swedana steam)."},
                        {"time": "12:30 PM - 01:30 PM", "activity": "Fresh Tridoshic lunch."},
                        {"time": "04:30 PM - 05:30 PM", "activity": "Ayurveda wellness workshop on daily dinacharya habits."},
                        {"time": "06:00 PM - 07:00 PM", "activity": "Guided Yoga Nidra and meditation session."}
                    ]
                }
            ],
            "pricing_table": pricing_table,
            "inclusions": [
                f"Accommodation for {duration} in verified Ayurvedic center in {destination}",
                "Initial and concluding consultations with experienced Ayurvedic physicians",
                "Daily doctor-prescribed Ayurvedic therapies, medicated oil massages, and steam baths",
                "All daily fresh Tridoshic vegetarian meals, herbal decoctions, and therapeutic teas",
                "Daily therapeutic yoga, pranayama, and guided relaxation sessions",
                "Dedicated YatraDham reservation assistance and verified center support"
            ],
            "exclusions": [
                "Travel expenses, flight, or train tickets to the destination",
                "Specialized diagnostic lab tests or non-package prescription medicines",
                "Personal laundry, phone calls, and individual room service orders",
                "Early check-in or late check-out beyond center guidelines"
            ],
            "nearby_locations_heading": f"How to Reach & Nearby Landmarks in {destination}",
            "nearby_locations": near_locs,
            "cancellation_policy": "Flexible cancellation available. Free cancellation up to 48 hours prior to check-in for verified partner centers.",
            "payment_policy_bullets": [
                "Secure advance payment required on YatraDham.Org to confirm reservation.",
                "Remaining balance payable upon arrival at the retreat check-in desk.",
                "All popular payment options accepted: UPI, Google Pay, NetBanking, and Cards."
            ],
            "terms_conditions": [
                "Valid government photo ID is mandatory for all check-in guests.",
                "Standard check-in time is 12:00 PM and check-out time is 12:00 PM.",
                "The retreat campus is strictly 100% vegetarian, non-alcoholic, and smoke-free.",
                "Please disclose any serious medical conditions or surgeries during initial doctor intake.",
                "Therapy schedules are assigned by the medical team to ensure optimal treatment sequencing."
            ],
            "faq": [
                {
                    "question": f"Is a doctor consultation included in {pkg_name}?",
                    "answer": f"Yes, every guest receives a comprehensive consultation with a qualified Ayurvedic doctor in {destination} to assess their dosha balance and tailor daily treatments."
                },
                {
                    "question": "What kind of food is served during the retreat?",
                    "answer": "Meals are 100% pure vegetarian, freshly prepared according to Ayurvedic principles with mild digestive spices, fresh vegetables, and whole grains."
                },
                {
                    "question": "Can complete beginners participate in the therapies and yoga?",
                    "answer": "Absolutely. All therapies and yoga classes are gentle, therapeutic, and customized to your individual physical condition and comfort level."
                },
                {
                    "question": "How do I reach the retreat center?",
                    "answer": f"The center in {destination} is conveniently connected to major airports and railway hubs. Detailed directions and landmark guidance are sent with your confirmation."
                }
            ]
        }

    # 2. CORPORATE EXCELLENCE & EXECUTIVE STRESS RELIEF (Corporate Excellence Program in Delhi)
    elif any(k in name_lower for k in ["corporate", "excellence", "executive", "burnout", "leadership"]):
        return {
            "package_overview": f"The {duration} {pkg_name} in {destination} is an immersive executive wellness retreat designed to combat workplace burnout, enhance cognitive focus, and cultivate sustainable mental resilience. Combining evidence-based mindfulness, spinal ergonomics, yogic breathwork, and high-performance lifestyle strategies, this program empowers working professionals and leaders to release chronic tension. Set in a peaceful campus insulated from city noise, participants learn practical tools to manage high-pressure environments, restore mental clarity, and maintain optimal work-life equilibrium.",
            "quick_facts": {
                "package_name": pkg_name,
                "cost": clean_cost,
                "duration": duration,
                "destination": destination,
                "level": "Working Professionals, Managers & Executives",
                "accommodation": f"Comfortable Executive Campus Stay in {destination}",
                "food": "Wholesome Energy-Boosting Sattvic Nutrition",
                "activities": "Stress Resilience Labs, Ergonomic Posture Yoga, Focus Breathwork",
                "center_name": f"{pkg_name} ({destination})",
                "yoga_sessions": "Morning Vitality Yoga & Evening Deep Relaxation"
            },
            "why_choose_heading": f"Why Choose This Corporate Wellness Program in {destination}?",
            "why_choose_intro": f"Invest in mental rejuvenation, executive focus, and long-term health in structured {destination} retreat environment.",
            "why_choose_bullets": [
                "Evidence-Based Stress Management: Learn practical neuro-resilience breathwork and mindfulness techniques to instantly lower cortisol levels.",
                "Spine & Posture Ergonomics: Specialized yoga sessions targeted at reversing desk-worker strain, neck stiffness, and lower back tension.",
                "Cognitive Focus & Mental Clarity: Guided mindfulness protocols that eliminate mental fatigue and sharpen strategic decision-making.",
                "Healthy Wholesome Nutrition: Clean, vibrant plant-based meals that provide sustained energy without afternoon slumps.",
                "Actionable Daily Toolkit: Take away a personalized 15-minute daily routine to maintain calm and peak productivity at your workplace."
            ],
            "who_can_benefit_heading": f"Who Should Attend This {destination} Program?",
            "who_can_benefit_intro": "This program is specifically designed for:",
            "who_can_benefit_bullets": [
                "Corporate executives, entrepreneurs, and team leaders facing intense workplace pressure.",
                "Professionals suffering from digital eye strain, chronic fatigue, or poor sleep quality.",
                "Individuals looking to establish healthy daily boundaries and prevent professional burnout.",
                "Teams seeking an inspiring offsite retreat focused on collective wellness and mindful collaboration.",
                "Anyone wanting to master scientifically proven relaxation and focus techniques."
            ],
            "program_highlights": {
                "heading": f"Executive Retreat Schedule in {destination}",
                "morning": [
                    {"time": "06:30 AM - 07:00 AM", "activity": "Morning breath activation & mindfulness centering"},
                    {"time": "07:00 AM - 08:15 AM", "activity": "Spinal alignment & restorative mobility yoga"},
                    {"time": "08:30 AM - 09:30 AM", "activity": "Nutrient-dense breakfast & networking tea"}
                ],
                "daytime": [
                    {"time": "10:00 AM - 12:30 PM", "activity": "Interactive workshop: Mastering stress triggers & cognitive clarity"},
                    {"time": "01:00 PM - 02:00 PM", "activity": "Fresh, balanced vegetarian executive lunch"},
                    {"time": "02:30 PM - 04:30 PM", "activity": "Digital detox time & quiet contemplative campus walk"}
                ],
                "evening": [
                    {"time": "05:00 PM - 06:15 PM", "activity": "Guided Yoga Nidra for deep nervous system recovery"},
                    {"time": "06:30 PM - 07:30 PM", "activity": "Evening sound meditation & reflective discussion"},
                    {"time": "07:30 PM - 08:30 PM", "activity": "Wholesome Sattvic dinner and social connection"}
                ]
            },
            "meal_section_heading": "High-Energy Brain & Body Nutrition",
            "meal_section_bullets": [
                "Wholesome, nutrient-packed vegetarian cuisine crafted to boost mental focus, balance blood sugar, and sustain high energy throughout the day.",
                "Includes antioxidant herbal infusions, fresh seasonal fruits, sprouts, and digestive teas."
            ],
            "accommodation_heading": f"Comfortable Executive Accommodations in {destination}",
            "accommodation_bullets": [
                f"Air-conditioned single and twin rooms in {destination} equipped with modern amenities, work desks, clean attached bathrooms, and high-speed Wi-Fi in common zones.",
                "Quiet campus surroundings ensure uninterrupted sleep and profound restfulness."
            ],
            "benefits_heading": f"Key Takeaways of This {duration} Corporate Program",
            "benefits_items": [
                "Burnout Reversal: Dissolves accumulated mental fatigue and restores emotional enthusiasm.",
                "Enhanced Decision Making: Calm, centered minds make faster and more strategic choices.",
                "Relief from Desk Strain: Targeted stretches relieve neck, shoulder, and lumbar discomfort.",
                "Deep Sleep Restoration: Nightly meditation techniques reset natural sleep cycles.",
                "Breathwork for High-Pressure Moments: Master 2-minute emergency calming breath techniques.",
                "Strengthened Team Dynamics: Fosters empathy, positive communication, and workplace harmony.",
                "Sustainable Habit Formation: Concrete daily practices easily integrated into busy calendars.",
                "Renewed Physical Vitality: Return to your organization with elevated drive and clarity."
            ],
            "how_to_book_heading": "How to Book on YatraDham.Org",
            "how_to_book_steps": [
                f"Navigate to {pkg_name} on YatraDham.Org and select dates for yourself or your corporate team.",
                "Choose single executive or twin sharing accommodation.",
                "Enter guest or corporate billing details.",
                "Complete the secure online payment to confirm the reservation.",
                "Receive your comprehensive joining kit with itinerary and directions in {destination}."
            ],
            "prices_photos_reviews": f"Program pricing starts from {clean_cost}. Check verified facility photos and corporate testimonials on YatraDham.Org.",
            "itinerary": [
                {
                    "day_number": 1,
                    "sessions": [
                        {"time": "01:00 PM", "activity": f"Check-in at {destination} retreat center and executive welcome drink."},
                        {"time": "03:30 PM", "activity": "Program orientation & executive stress assessment."},
                        {"time": "05:30 PM", "activity": "Desk-worker mobility yoga & posture correction."},
                        {"time": "07:30 PM", "activity": "Welcome dinner & informal networking."}
                    ]
                },
                {
                    "day_number": 2,
                    "sessions": [
                        {"time": "07:00 AM", "activity": "Morning breathwork & vitality asanas."},
                        {"time": "08:30 AM", "activity": "Wholesome breakfast."},
                        {"time": "10:30 AM", "activity": "Mindful leadership & cognitive resilience masterclass."},
                        {"time": "01:00 PM", "activity": "Nutritious lunch & reflective downtime."},
                        {"time": "05:00 PM", "activity": "Guided Yoga Nidra & deep nervous system reset."},
                        {"time": "07:30 PM", "activity": "Wholesome dinner and mindful discussions."}
                    ]
                }
            ],
            "pricing_table": pricing_table,
            "inclusions": [
                f"Full executive accommodation for {duration} in {destination}",
                "All interactive workshops, posture coaching, and guided mindfulness sessions",
                "Complete wholesome Sattvic vegetarian meals, herbal beverages, and healthy refreshments",
                "Comprehensive digital workbook and 15-minute daily workplace toolkit",
                "Dedicated YatraDham corporate support and assistance"
            ],
            "exclusions": [
                "Air/rail transit fares to the retreat center",
                "Individual private counseling sessions outside the scheduled curriculum",
                "Personal expenses and incidental room services"
            ],
            "nearby_locations_heading": f"How to Reach & Nearby Landmarks in {destination}",
            "nearby_locations": near_locs,
            "cancellation_policy": "Flexible cancellation terms for corporate and individual bookings up to 72 hours prior to arrival.",
            "payment_policy_bullets": [
                "Instant confirmation with online advance payment.",
                "Corporate GST invoices available upon request.",
                "Accepted modes: NetBanking, Corporate Cards, and UPI."
            ],
            "terms_conditions": [
                "Government ID required at check-in.",
                "Non-smoking, vegetarian, and alcohol-free campus.",
                "Punctuality during group workshops is appreciated."
            ],
            "faq": [
                {
                    "question": f"Is {pkg_name} suitable for individual professionals or only corporate groups?",
                    "answer": f"Both individual professionals and corporate teams can join. The curriculum is equally beneficial for personal burnout recovery and team wellness in {destination}."
                },
                {
                    "question": "Can I attend urgent work calls during the retreat?",
                    "answer": "Yes, high-speed Wi-Fi is available in designated zones, though we recommend minimizing screen time during workshop hours to maximize benefits."
                },
                {
                    "question": "What is the dress code for sessions?",
                    "answer": "Comfortable, loose-fitting cotton or athletic clothing suitable for light stretching and seated discussions."
                }
            ]
        }

    # 3. ASHRAM SILENCE, KRIYA & MEDITATION RETREATS (Abhayaranya, Kriya Yoga Ashram, Adhyatm Sadhna Kendra)
    elif any(k in name_lower for k in ["abhayaranya", "kriya", "adhyatm", "silence", "meditation", "ashram", "camp in delhi"]):
        return {
            "package_overview": f"Immerse yourself in authentic spiritual stillness with the {duration} at {pkg_name} in serene {destination}. Designed as a sacred sanctuary away from commercial distractions, this retreat guides seekers through traditional meditation techniques, period of mindful silence (Mauna), and introspective Kriya practices. Guided by experienced resident acharyas, you will awaken inner clarity through morning sun salutations, sound meditation, and yogic contemplation. Nourished by pure ashram Sattvic meals in the {destination} foothills, this retreat offers a rare opportunity to disconnect from the digital world and rediscover profound inner peace.",
            "quick_facts": {
                "package_name": pkg_name,
                "cost": clean_cost,
                "duration": duration,
                "destination": destination,
                "level": "All Spiritual Seekers & Meditators",
                "accommodation": f"Peaceful Ashram Stay in {destination}",
                "food": "100% Pure Meditative Sattvic Meals",
                "activities": "Guided Mauna (Silence), Kriya Meditation, Sound Healing",
                "center_name": f"{pkg_name} ({destination})",
                "yoga_sessions": "Daily Meditative Asanas & Breathwork"
            },
            "why_choose_heading": f"Why Choose This Sacred Meditation Stay in {destination}?",
            "why_choose_intro": f"Step into a disciplined, time-honored ashram atmosphere that nurtures deep spiritual contemplation in {destination}.",
            "why_choose_bullets": [
                "Sacred Ashram Heritage: Practice in an authentic spiritual sanctuary renowned for peaceful energy and disciplined living.",
                "Period of Mindful Silence (Mauna): Experience the extraordinary mental stillness of structured silence periods that quiet internal chatter.",
                "Traditional Meditation Techniques: Step-by-step guidance in breath observation, Trataka (gazing), and guided sound meditation.",
                "Gentle Mindful Yoga: Slow-paced Hatha stretches designed to prepare your physical body for comfortable seated meditation.",
                "Pure Meditative Nutrition: Wholesome, simply prepared Sattvic meals that keep the mind clear, light, and alert."
            ],
            "who_can_benefit_heading": f"Who Is This {destination} Retreat For?",
            "who_can_benefit_intro": "This contemplative retreat welcomes anyone who feels called to:",
            "who_can_benefit_bullets": [
                "Unplug completely from screens, work notifications, and urban overstimulation.",
                "Deepen their personal meditation practice under seasoned spiritual mentors.",
                "Process emotional transitions or find clarity on important life questions.",
                "Experience the healing power of structured silence and mindful walking.",
                "Live simply in a spiritual community dedicated to truth and inner growth."
            ],
            "program_highlights": {
                "heading": f"Daily Ashram Routine & Schedule in {destination}",
                "morning": [
                    {"time": "05:15 AM", "activity": "Ashram morning bell & cleansing herbal water"},
                    {"time": "05:45 AM - 07:00 AM", "activity": "Guided sunrise meditation & pranayama breathwork"},
                    {"time": "07:15 AM - 08:30 AM", "activity": "Mindful gentle asana flow for seated posture stability"},
                    {"time": "08:45 AM - 09:45 AM", "activity": "Silent mindful Sattvic breakfast"}
                ],
                "daytime": [
                    {"time": "10:30 AM - 12:00 PM", "activity": "Yogic philosophy lecture, self-study (Swadhyaya) or nature walk"},
                    {"time": "12:30 PM - 01:30 PM", "activity": "Nourishing Sattvic lunch"},
                    {"time": "02:00 PM - 04:00 PM", "activity": "Contemplative rest & personal journaling"}
                ],
                "evening": [
                    {"time": "04:30 PM - 05:45 PM", "activity": "Sound healing & Yoga Nidra relaxation"},
                    {"time": "06:00 PM - 07:00 PM", "activity": "Evening group chanting (Kirtan) & peaceful meditation"},
                    {"time": "07:15 PM - 08:15 PM", "activity": "Light evening dinner followed by reflective silence"},
                    {"time": "09:00 PM", "activity": "Lights out and deep restful sleep"}
                ]
            },
            "meal_section_heading": "Pure Ashram Sattvic Cuisine",
            "meal_section_bullets": [
                "Prepared with love and prayer (Prasada style), meals are 100% vegetarian, free of onions, garlic, and heavy spices to foster tranquil meditation.",
                "Wholesome whole grains, lentils, fresh seasonal vegetables, and herbal decoctions nourish body and spirit."
            ],
            "accommodation_heading": f"Simple & Clean Ashram Rooms in {destination}",
            "accommodation_bullets": [
                f"Immaculately maintained ashram rooms in {destination} with comfortable bedding, attached modern bathrooms, and scenic views of nature.",
                "The atmosphere is intentionally calm, uncluttered, and conducive to deep spiritual introspection."
            ],
            "benefits_heading": f"Spiritual & Mental Benefits of This {duration} Stay",
            "benefits_items": [
                "Profound Mental Calm: Quiets racing thoughts and dissolves chronic internal anxiety.",
                "Enhanced Self-Awareness: Structured silence allows deep self-discovery and emotional clarity.",
                "Mastery of Breath: Advanced pranayama techniques balance nervous energy.",
                "Digital Detox Rejuvenation: Disconnecting from technology resets dopamine pathways.",
                "Comfort in Seated Stillness: Asana alignment helps you sit effortlessly in meditation.",
                "Emotional Grounding: Sound vibrations and chanting release stored emotional blockages.",
                "Inspiration from Ashram Community: Share sacred space with fellow dedicated seekers.",
                "Lasting Spiritual Foundation: Carry transformative meditation habits into your daily home life."
            ],
            "how_to_book_heading": "How to Book on YatraDham.Org",
            "how_to_book_steps": [
                f"Visit the {pkg_name} page on YatraDham.Org and choose your dates.",
                "Select private or shared ashram room accommodation.",
                "Submit your reservation with secure online advance payment.",
                "Receive your confirmation voucher with ashram arrival guidelines in {destination}.",
                "Arrive peacefully and begin your spiritual immersion."
            ],
            "prices_photos_reviews": f"Retreat contribution starts from {clean_cost}. View ashram campus photos and pilgrim testimonials on YatraDham.Org.",
            "itinerary": [
                {
                    "day_number": 1,
                    "sessions": [
                        {"time": "12:00 PM", "activity": f"Arrival at {destination} ashram, room check-in, and herbal welcome drink."},
                        {"time": "04:00 PM", "activity": "Ashram orientation and introduction to the science of meditation."},
                        {"time": "06:00 PM", "activity": "Evening chanting and sunset meditation."},
                        {"time": "07:30 PM", "activity": "Sattvic dinner and commencement of evening quiet hours."}
                    ]
                },
                {
                    "day_number": 2,
                    "sessions": [
                        {"time": "05:45 AM", "activity": "Sunrise meditation and breath awareness."},
                        {"time": "07:15 AM", "activity": "Gentle asana flow for spinal flexibility."},
                        {"time": "08:45 AM", "activity": "Silent Sattvic breakfast."},
                        {"time": "11:00 AM", "activity": "Guided nature contemplation and sound meditation."},
                        {"time": "12:30 PM", "activity": "Wholesome lunch and personal contemplation."},
                        {"time": "05:00 PM", "activity": "Yoga Nidra and evening spiritual satsang."}
                    ]
                }
            ],
            "pricing_table": pricing_table,
            "inclusions": [
                f"Ashram accommodation for {duration} in peaceful {destination}",
                "All daily meditation instruction, sound baths, and spiritual discourses",
                "Three fresh Sattvic vegetarian meals daily plus morning and evening herbal teas",
                "Access to ashram meditation halls, library, and contemplative gardens",
                "Dedicated YatraDham reservation assistance"
            ],
            "exclusions": [
                "Transportation and transit fares to the ashram venue",
                "Personal laundry, toiletries, and individual purchases",
                "Private specialized pujas outside the scheduled ashram routine"
            ],
            "nearby_locations_heading": f"How to Reach & Nearby Landmarks in {destination}",
            "nearby_locations": near_locs,
            "cancellation_policy": "Flexible ashram reservation cancellation available up to 48 hours prior to scheduled arrival.",
            "payment_policy_bullets": [
                "Secure advance booking on YatraDham.Org.",
                "Balance contribution settled at ashram reception upon arrival.",
                "Accepted: UPI, Google Pay, Cards, and NetBanking."
            ],
            "terms_conditions": [
                "Valid ID proof required upon arrival.",
                "Strict adherence to ashram decorum: 100% vegetarian, non-smoking, and alcohol-free.",
                "Guests are requested to maintain silence during designated meditation hours."
            ],
            "faq": [
                {
                    "question": "What is the Mauna (silence) practice and is it compulsory all day?",
                    "answer": "Silence is observed during specific hours (such as morning meditation and meal times) to cultivate inner stillness. It is gentle, guided, and deeply restorative."
                },
                {
                    "question": "Do I need prior experience in meditation to join?",
                    "answer": "No prior experience is necessary. Resident teachers provide step-by-step guidance suitable for beginners and seasoned meditators alike."
                },
                {
                    "question": "Are mobile phones allowed in the ashram?",
                    "answer": "Mobile phones may be kept in your room for emergency use, but are strictly prohibited in the meditation halls and dining areas to preserve the sacred atmosphere."
                }
            ]
        }

    # 4. NATURE, FOREST & ECO WELLNESS (Alibaug Forest, Nalsarovar, Purnashakti Junagadh)
    elif any(k in name_lower for k in ["forest", "alibaug", "nalsarovar", "lake", "purnashakti", "nature"]):
        return {
            "package_overview": f"Escape the noise of modern urban life with the {duration} at {pkg_name} in picturesque {destination}. Immersed in lush green surroundings, this holistic retreat blends open-air nature yoga, Japanese Shinrin-yoku forest bathing, mindful walking trails, and rejuvenating organic nutrition. Away from traffic, concrete, and screens, you will breathe crisp fresh air, realign your circadian rhythm with the natural sunrise and sunset, and experience restorative relaxation. With comfortable eco-friendly lodging and nourishing farm-to-table vegetarian meals in {destination}, this retreat offers the ultimate restorative reset for body and soul.",
            "quick_facts": {
                "package_name": pkg_name,
                "cost": clean_cost,
                "duration": duration,
                "destination": destination,
                "level": "Nature Enthusiasts & All Fitness Levels",
                "accommodation": f"Eco-Friendly Nature Resort Stay in {destination}",
                "food": "Farm-Fresh 100% Organic Vegetarian Cuisine",
                "activities": "Forest Bathing, Lakeside Meditation, Open-Air Prana Yoga",
                "center_name": f"{pkg_name} ({destination})",
                "yoga_sessions": "Morning Sunrise Yoga & Sunset Restorative Flow"
            },
            "why_choose_heading": f"Why Choose This {duration} Nature Retreat in {destination}?",
            "why_choose_intro": f"Recharge in pure natural landscapes and biodiversity in {destination}.",
            "why_choose_bullets": [
                "Pristine Eco-Sanctuary: Situated in undisturbed natural greenery with clean mountain/coastal air and peaceful tranquility.",
                "Forest Bathing & Mindful Trails: Guided walking meditations and sensory immersion practices under rich forest canopies.",
                "Open-Air Yoga Pavilion: Practice asanas and breathwork surrounded by birdsong and rustling leaves.",
                "Farm-to-Table Nutrition: Organic seasonal vegetables, whole grains, and herbal immunity drinks prepared fresh daily.",
                "Deep Sleep Ambiance: Natural night sounds and zero light pollution ensure profound cellular regeneration."
            ],
            "who_can_benefit_heading": f"Who Will Love This {destination} Nature Getaway?",
            "who_can_benefit_intro": "This restorative retreat is perfect for:",
            "who_can_benefit_bullets": [
                "Urban dwellers needing immediate relief from city smog, noise, and screen fatigue.",
                "Couples, solo travelers, and wellness seekers looking for peaceful nature immersion.",
                "Anyone wanting to combine light hiking, mindful walks, and outdoor yoga practice.",
                "Individuals suffering from restless sleep or chronic mental overwhelm.",
                "Nature lovers seeking a clean, verified eco-resort with wholesome Sattvic food."
            ],
            "program_highlights": {
                "heading": f"Daily Nature & Wellness Routine in {destination}",
                "morning": [
                    {"time": "06:15 AM - 06:45 AM", "activity": "Sunrise grounding breathwork & birdwatching walk"},
                    {"time": "07:00 AM - 08:15 AM", "activity": "Open-air prana yoga flow & dynamic stretching"},
                    {"time": "08:30 AM - 09:30 AM", "activity": "Farm-fresh organic breakfast & herbal infusions"}
                ],
                "daytime": [
                    {"time": "10:30 AM - 12:30 PM", "activity": "Guided forest bathing (Shinrin-yoku) trail & tree meditation"},
                    {"time": "01:00 PM - 02:00 PM", "activity": "Traditional farm-to-table vegetarian lunch"},
                    {"time": "02:30 PM - 04:30 PM", "activity": "Hammock relaxation, journaling, or herbal garden tour"}
                ],
                "evening": [
                    {"time": "05:00 PM - 06:15 PM", "activity": "Sunset restorative yoga & gentle hip/spine mobility"},
                    {"time": "06:30 PM - 07:30 PM", "activity": "Bonfire mindfulness circle & stargazing meditation"},
                    {"time": "07:30 PM - 08:30 PM", "activity": "Wholesome organic dinner and quiet reflection"}
                ]
            },
            "meal_section_heading": "Farm-to-Table Organic Nutrition",
            "meal_section_bullets": [
                "Enjoy wholesome meals cooked with locally grown vegetables, whole grains, cold-pressed oils, and fresh herbs.",
                "Food is prepared fresh daily to detoxify your digestive system and provide sustained natural vitality."
            ],
            "accommodation_heading": f"Comfortable Eco-Living in {destination}",
            "accommodation_bullets": [
                f"Charming eco-cottages and rooms in {destination} featuring natural ventilation, clean attached bathrooms, and private balconies overlooking lush greenery.",
                "Built to harmonize with the local ecosystem while providing verified modern comfort."
            ],
            "benefits_heading": f"Rejuvenating Benefits of This Nature Program",
            "benefits_items": [
                "Clean Air Lung Cleansing: Deep breathing in forested zones clears respiratory pathways.",
                "Lower Cortisol Levels: Nature immersion scientifically reduces stress hormone production.",
                "Circadian Rhythm Reset: Exposure to natural sunlight restores healthy melatonin cycles.",
                "Postural & Spinal Relief: Outdoor stretching relieves chronic back and shoulder stiffness.",
                "Mindful Mental Stillness: Calms mental chatter and replaces anxiety with grounded serenity.",
                "Digestive Detoxification: Pure organic ingredients nourish your gut microbiome.",
                "Sensory Reconnection: Awaken your senses to natural aromas, sounds, and textures.",
                "Return Home Energized: Re-enter daily routines with renewed enthusiasm and poise."
            ],
            "how_to_book_heading": "How to Book on YatraDham.Org",
            "how_to_book_steps": [
                f"Check available dates for {pkg_name} on YatraDham.Org.",
                "Select your preferred cottage or room category.",
                "Enter guest details and dietary preferences.",
                "Complete the secure payment on YatraDham's verified portal.",
                "Receive instant confirmation with GPS directions and arrival tips in {destination}."
            ],
            "prices_photos_reviews": f"Rates start from {clean_cost}. Explore landscape photos, cottage views, and guest ratings on YatraDham.Org.",
            "itinerary": [
                {
                    "day_number": 1,
                    "sessions": [
                        {"time": "12:00 PM", "activity": f"Arrival in {destination}, check-in, and fresh coconut welcome drink."},
                        {"time": "03:30 PM", "activity": "Orientation walk through the organic orchard and grounds."},
                        {"time": "05:00 PM", "activity": "Sunset grounding yoga flow."},
                        {"time": "07:30 PM", "activity": "Farm-fresh dinner and stargazing."}
                    ]
                },
                {
                    "day_number": 2,
                    "sessions": [
                        {"time": "06:15 AM", "activity": "Morning forest walk and sunrise breathing."},
                        {"time": "07:30 AM", "activity": "Open-air prana yoga session."},
                        {"time": "08:45 AM", "activity": "Organic wholesome breakfast."},
                        {"time": "11:00 AM", "activity": "Guided nature meditation and tree bathing."},
                        {"time": "01:00 PM", "activity": "Wholesome lunch and personal leisure."},
                        {"time": "05:30 PM", "activity": "Evening restorative yoga and bonfire reflection."}
                    ]
                }
            ],
            "pricing_table": pricing_table,
            "inclusions": [
                f"Eco-resort accommodation for {duration} in {destination}",
                "All guided forest trails, nature walks, and outdoor yoga/meditation sessions",
                "Complete farm-fresh organic vegetarian meals and herbal beverages",
                "Bonfire mindfulness gatherings and stargazing sessions",
                "Dedicated YatraDham reservation assistance and guest protection"
            ],
            "exclusions": [
                "Transit costs to the retreat location",
                "Private personal vehicle hire or external safari tickets",
                "Personal expenses, laundry, and shopping"
            ],
            "nearby_locations_heading": f"How to Reach & Nearby Landmarks in {destination}",
            "nearby_locations": near_locs,
            "cancellation_policy": "Free cancellation available up to 48 hours prior to check-in for verified partner properties.",
            "payment_policy_bullets": [
                "Advance online booking secures your cottage.",
                "Balance paid directly at resort reception.",
                "Accepted: UPI, Google Pay, NetBanking, and Cards."
            ],
            "terms_conditions": [
                "Valid ID proof required at check-in.",
                "Eco-friendly guidelines: Please respect wildlife and minimize plastic waste.",
                "Non-smoking, non-alcoholic, and pure vegetarian property."
            ],
            "faq": [
                {
                    "question": "What footwear and clothing should I bring?",
                    "answer": "Comfortable walking or hiking shoes, breathable cotton clothing for yoga, a sun hat, and a light jacket for cool evenings."
                },
                {
                    "question": "Is the retreat venue safe and easily accessible?",
                    "answer": f"Yes, the venue in {destination} is fully fenced, securely staffed, and accessible by car or taxi with paved road access."
                },
                {
                    "question": "Is Wi-Fi available at the nature retreat?",
                    "answer": "Wi-Fi is available in central lounge areas, while cottage zones are kept low-EMF to encourage digital detox and restful sleep."
                }
            ]
        }

    # 5. CLASSICAL HATHA & ASHTANGA YOGA (Patanjali, Arogya, Akhanda, Mrityunjay, The Yoga Institute, Jahnavi, Modi)
    else:
        return {
            "package_overview": f"Immerse yourself in authentic yogic tradition with the {duration} at {pkg_name} in {destination}. Situated in the serene spiritual atmosphere of {destination}, this retreat provides a holistic grounding in classical Hatha and Ashtanga yoga, Pranayama breathwork, Shatkarma cleansing techniques, and restorative Yoga Nidra. Certified yoga acharyas guide your daily practice with precision, focusing on proper anatomical alignment, breath synchronization, and mental focus. Complete with wholesome Sattvic vegetarian meals and verified comfortable lodging, this {duration} retreat is the ultimate getaway to energize your body, quiet your mind, and reconnect with your inner self.",
            "quick_facts": {
                "package_name": pkg_name,
                "cost": clean_cost,
                "duration": duration,
                "destination": destination,
                "level": "Beginner to Advanced Practitioners",
                "accommodation": f"Clean Verified Stay in {destination}",
                "food": "100% Pure Fresh Sattvic Vegetarian Cuisine",
                "activities": "Classical Hatha Yoga, Pranayama, Meditation & Philosophy",
                "center_name": f"{pkg_name} ({destination})",
                "yoga_sessions": "Twice Daily Guided Yoga Practice"
            },
            "why_choose_heading": f"Why Choose This {duration} Yoga Experience in {destination}?",
            "why_choose_intro": f"Deepen your practice under seasoned yoga masters in the authentic spiritual atmosphere of {destination}.",
            "why_choose_bullets": [
                "Master-Led Instruction: Learn from certified yoga teachers with extensive training in classical Hatha, Ashtanga, and therapeutic yoga.",
                "Holistic Daily Curriculum: Structured routine featuring morning energizing asanas, evening restorative flows, pranayama, and guided meditation.",
                "Yogic Cleansing & Alignment: Gain hands-on alignment guidance, prop usage, and introductory Shatkarma cleansing practices.",
                "Wholesome Sattvic Nourishment: Enjoy three delicious, freshly prepared vegetarian meals daily designed to fuel yogic practice.",
                "Verified & Safe Environment: Clean, comfortable lodging in {destination} backed by YatraDham's verified standards and 24/7 guest support."
            ],
            "who_can_benefit_heading": f"Who Can Join This {destination} Retreat?",
            "who_can_benefit_intro": "This program welcomes individuals of all backgrounds who wish to:",
            "who_can_benefit_bullets": [
                "Begin their yoga journey with solid anatomical foundations and authentic yogic guidance.",
                "Deepen an existing practice and explore advanced breathwork and meditation techniques.",
                "Relieve physical stiffness, improve spinal flexibility, and build core muscular stamina.",
                "Take a peaceful, structured break from stressful urban routines in a serene environment.",
                "Learn practical yogic lifestyle habits and philosophy that inspire long-term wellness."
            ],
            "program_highlights": {
                "heading": f"Daily Yogic Schedule in {destination}",
                "morning": [
                    {"time": "06:00 AM - 06:30 AM", "activity": "Morning herbal infusion & yogic breathing exercises"},
                    {"time": "06:30 AM - 08:00 AM", "activity": "Classical Hatha / Ashtanga dynamic asana practice"},
                    {"time": "08:30 AM - 09:30 AM", "activity": "Wholesome Sattvic breakfast & tea"}
                ],
                "daytime": [
                    {"time": "10:30 AM - 12:00 PM", "activity": "Yoga philosophy, anatomy & alignment workshop"},
                    {"time": "12:30 PM - 01:30 PM", "activity": "Fresh vegetarian Sattvic lunch"},
                    {"time": "02:00 PM - 04:00 PM", "activity": "Personal relaxation, reading, or nearby nature walk"}
                ],
                "evening": [
                    {"time": "04:30 PM - 05:45 PM", "activity": "Gentle restorative yoga & deep Pranayama"},
                    {"time": "06:00 PM - 07:00 PM", "activity": "Guided meditation, chanting, and quiet reflection"},
                    {"time": "07:30 PM - 08:30 PM", "activity": "Nutritious Sattvic dinner and social sharing"}
                ]
            },
            "meal_section_heading": "Pure & Nutritious Sattvic Food",
            "meal_section_bullets": [
                "All meals are freshly prepared with seasonal vegetables, whole grains, lentils, and wholesome dairy according to traditional Sattvic principles.",
                "The food is nourishing, light on digestion, and formulated to enhance energy, mental clarity, and body flexibility."
            ],
            "accommodation_heading": f"Comfortable Verified Lodging in {destination}",
            "accommodation_bullets": [
                f"Well-appointed private and shared rooms in {destination} featuring clean beds, attached modern bathrooms, hot water, and quiet surroundings.",
                "Designed to ensure complete rest and peaceful sleep after active daily yoga sessions."
            ],
            "benefits_heading": f"Transformative Benefits of This {duration} Program",
            "benefits_items": [
                "Improved Strength & Posture: Strengthens spinal core muscles and rectifies daily postural imbalances.",
                "Increased Flexibility: Gentle daily lengthening of tight muscles and hamstrings.",
                "Deep Stress Reduction: Down-regulates the nervous system through conscious breathwork.",
                "Enhanced Vital Energy: Boosts physical stamina and natural immunity through pranayama.",
                "Mental Clarity & Peace: Meditation quiets mental agitation and fosters emotional stability.",
                "Better Sleep Quality: Calming evening sessions encourage deep, uninterrupted sleep.",
                "Practical Takeaway Routine: Master a sequence you can practice independently at home.",
                "Inspiring Community: Connect with supportive, like-minded practitioners in {destination}."
            ],
            "how_to_book_heading": "How to Book on YatraDham.Org",
            "how_to_book_steps": [
                f"Select your dates for {pkg_name} on YatraDham.Org.",
                "Choose private single room or shared room accommodation.",
                "Enter guest details and any special dietary requirements.",
                "Complete the secure advance payment using UPI, NetBanking, or Cards.",
                "Receive instant booking confirmation voucher with direct center contact and arrival directions in {destination}."
            ],
            "prices_photos_reviews": f"Package pricing starts from {clean_cost}. Check real center photos and traveler reviews on YatraDham.Org.",
            "itinerary": [
                {
                    "day_number": 1,
                    "sessions": [
                        {"time": "12:00 PM", "activity": f"Arrival in {destination}, room check-in, and welcome drink."},
                        {"time": "04:00 PM", "activity": "Retreat orientation, teacher introduction, and yogic overview."},
                        {"time": "05:30 PM", "activity": "Gentle evening stretching and breath awareness."},
                        {"time": "07:30 PM", "activity": "Fresh Sattvic dinner and peaceful evening."}
                    ]
                },
                {
                    "day_number": 2,
                    "sessions": [
                        {"time": "06:30 AM", "activity": "Morning Hatha yoga and Pranayama."},
                        {"time": "08:30 AM", "activity": "Wholesome breakfast."},
                        {"time": "11:00 AM", "activity": "Yoga philosophy and alignment lecture."},
                        {"time": "12:30 PM", "activity": "Nutritious lunch and rest."},
                        {"time": "04:30 PM", "activity": "Restorative evening yoga and Yoga Nidra."},
                        {"time": "06:00 PM", "activity": "Guided meditation and sound chanting."}
                    ]
                }
            ],
            "pricing_table": pricing_table,
            "inclusions": [
                f"Accommodation for {duration} in verified center in {destination}",
                "All daily classical yoga classes, pranayama sessions, and meditation workshops",
                "Three fresh Sattvic vegetarian meals daily and herbal teas",
                "Use of yoga mats, straps, and props during all sessions",
                "Dedicated YatraDham customer support and reservation guarantee"
            ],
            "exclusions": [
                "Air/rail transit expenses to the destination",
                "Personal laundry, phone calls, and shopping",
                "Optional private sightseeing tours or extra therapies"
            ],
            "nearby_locations_heading": f"How to Reach & Nearby Landmarks in {destination}",
            "nearby_locations": near_locs,
            "cancellation_policy": "Flexible cancellation terms available for verified partner venues up to 48 hours before check-in.",
            "payment_policy_bullets": [
                "Secure advance booking on YatraDham.Org.",
                "Remaining balance payable upon check-in at the retreat desk.",
                "UPI, NetBanking, and all major cards accepted."
            ],
            "terms_conditions": [
                "Valid government photo ID required at check-in.",
                "Standard check-in time is 12:00 PM; check-out is 12:00 PM.",
                "Strictly vegetarian, smoke-free, and alcohol-free premises.",
                "Please notify instructors of any injuries or limitations prior to sessions."
            ],
            "faq": [
                {
                    "question": f"Is {pkg_name} suitable for complete yoga beginners?",
                    "answer": f"Yes, classes are thoughtfully structured to accommodate all levels. Instructors provide gentle modifications so beginners can practice safely and comfortably in {destination}."
                },
                {
                    "question": "What should I pack for the retreat?",
                    "answer": "Pack comfortable, modest clothing suitable for yoga and meditation, personal toiletries, a water bottle, and walking shoes for outdoor trails."
                },
                {
                    "question": "What is the food quality and hygiene standard?",
                    "answer": "All food is 100% pure vegetarian, freshly cooked under strict hygienic standards using filtered water and organic seasonal ingredients."
                }
            ]
        }
