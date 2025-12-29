import streamlit as st
from datetime import datetime

# --- إعدادات الصفحة ---
st.set_page_config(page_title="نبيه | Nabih", layout="centered")

# --- المحرك الذكي (Nabih Engine) ---
class NabihEngine:
    def calculate_projection(self, current_reading, day_of_month, total_days_in_month=30):
        # تجنب القسمة على صفر
        if day_of_month == 0: day_of_month = 1
        
        # حساب المعدل اليومي
        daily_avg = current_reading / day_of_month
        
        # توقع القراءة النهائية
        projected_reading = daily_avg * total_days_in_month
        
        # حسبة تقريبية للتكلفة (متوسط 23 هللة للشريحة السكنية مع الضريبة)
        # هذا نموذج مبسط MVP
        cost = projected_reading * 0.23 
        return daily_avg, cost

    def simulate_action(self, projected_cost, action_type):
        savings = 0
        if action_type == "AC_CUT":
            savings = projected_cost * 0.15 # توفير 15% تقديري
        elif action_type == "PEAK_SHIFT":
            savings = projected_cost * 0.05 # توفير 5% تقديري
        return projected_cost - savings, savings

# تهيئة المحرك
engine = NabihEngine()

# --- واجهة المستخدم (UI) ---
st.title("💡 نَبِيه | Nabih")
st.write("رفيقك الذكي.. عشان فاتورتك ما تفاجئك")
st.divider()

# --- منطقة الإدخال ---
with st.container(border=True):
    st.subheader("1️⃣ كم واصل عدادك؟")
    current_cost = st.number_input("سجل قراءة العداد الحالية (Kwh):", min_value=0.0, value=0.0)

    st.subheader("2️⃣ كم حدك الشهري؟")
    col1, col2 = st.columns(2)
    with col1:
        days_passed = st.slider("اليوم كم بالشهر؟", 1, 30, datetime.now().day)
    with col2:
        shock_limit = st.number_input("المبلغ اللي يزعلّك تجاوزه (ريال)", value=500)

    calculate_btn = st.button("يا نبيه.. طمنّي 📊", type="primary", use_container_width=True)

# --- منطقة النتائج ---
if calculate_btn:
    if current_cost > 0:
        daily_avg, projected = engine.calculate_projection(current_cost, days_passed)
        shock_gap = projected - shock_limit
        
        # منطق الألوان (إشارة المرور)
        if shock_gap > 0:
            mood_color = "#be123c" # أحمر
            mood_msg = f"انتبه! بتتجاوز الحد بـ {shock_gap:.0f} ريال"
        elif shock_gap > -50:
            mood_color = "#f59e0b" # برتقالي
            mood_msg = "انتبه.. أنت قريب من الخطر!"
        else:
            mood_color = "#0f766e" # أخضر
            mood_msg = "يا سلام عليك.. وضعك نبيه وممتاز"

        # عرض الكارت الملون
        st.markdown(f"""
            <div style='background-color: {mood_color}; padding: 15px; border-radius: 10px; color: white; text-align: center; margin-bottom: 10px;'>
                <h3 style='margin:0;'>{mood_msg}</h3>
            </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        c1.metric("فاتورة نهاية الشهر المتوقعة", f"{projected:.0f} ريال")
        c2.metric("حدك المستهدف", f"{shock_limit} ريال")
        
        st.divider()
        
        # المحاكاة (الذكاء السلوكي)
        st.subheader("🤔 جرب توفّر مع نبيه")
        if st.button("لو طفيت مكيف واحد ساعة يومياً؟"):
            new_proj, savings = engine.simulate_action(projected, "AC_CUT")
            st.success(f"ممكن توفر حوالي: **{savings:.0f} ريال** وتصير فاتورتك {new_proj:.0f} ريال")
            
    else:
        st.warning("فضلاً، أدخل قراءة العداد أولاً.")

st.markdown("---")
st.caption("© 2025 نَبِيه (Nabih) - النسخة التجريبية MVP")