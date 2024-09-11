from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # นำเข้า CORS Middleware
from pydantic import BaseModel
import joblib
import pandas as pd

# Load model and scaler
model = joblib.load('rf_model.joblib')
scaler = joblib.load('scaler.joblib')

# Load columns used in training
columns_to_use = joblib.load('columns_to_use.joblib')

app = FastAPI()

# CORS configuration to allow requests from the frontend
origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://127.0.0.1:5500",
    "http://localhost:3000",
    "http://127.0.0.1:8000" 
    # เพิ่มโดเมนของคุณหากรันใน production เช่น "https://myapp.com"
]

# ตั้งค่า CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # อนุญาตทุกวิธีการ เช่น GET, POST, OPTIONS
    allow_headers=["*"],  # อนุญาตทุก headers
)

class InputData(BaseModel):
    BRCA: list[str]
    BMI_GROUP: dict[str, float]
    AGE_GROUP: int
    PROVINCE_GROUP: list[str]
    GENDER_N: str

@app.post("/predict/")
def predict(data: InputData):
    try:
        # Convert input data to DataFrame
        df = pd.DataFrame([data.dict().values()], columns=data.dict().keys())

        # Process BRCA
        brca_mapping = {'negative': '1:N', 'positive': '2:P'}
        df['BRCA'] = [brca_mapping.get(val, '0:Unknown') for val in data.BRCA]

        # Process BMI_GROUP
        weight = data.BMI_GROUP.get('weight', 0)
        height = data.BMI_GROUP.get('height', 0)
        bmi = weight / (height ** 2) if height > 0 else 0
        if bmi <= 18.5:
            bmi_group = '1:<19'
        elif 19 <= bmi <= 24.9:
            bmi_group = '2:<25'
        elif 25 <= bmi <= 29.9:
            bmi_group = '3:<30'
        elif bmi < 99:
            bmi_group = '4:<99'
        else:
            bmi_group = '0:No'
        df['BMI_GROUP'] = bmi_group

        # Process AGE_GROUP
        age = data.AGE_GROUP
        if age < 30:
            age_group = '1:<30'
        elif 30 <= age <= 39:
            age_group = '2:<40'
        elif 40 <= age <= 49:
            age_group = '3:<50'
        elif age < 99:
            age_group = '4:<99'
        else:
            age_group = '0:Unknown'
        df['AGE_GROUP'] = age_group

        # Process PROVINCE_GROUP
        province_mapping = {
            'ยะลา': 1, 'ปัตตานี': 1, 'นราธิวาส': 1,
            'สงขลา': 2, 'สตูล': 2,
            'พังงา': 3, 'พัทลุง': 3,
            'อื่นๆ': 4
        }
        province_group = province_mapping.get(data.PROVINCE_GROUP[0], 4)
        df['PROVINCE_GROUP'] = province_group

        # Process GENDER_N
        gender_mapping = {'Male': 0, 'Female': 1}
        df['GENDER_N'] = gender_mapping.get(data.GENDER_N, -1)

        # Convert categorical variables to dummies
        df = pd.get_dummies(df, drop_first=True)
        df = df.reindex(columns=columns_to_use, fill_value=0)

        # Scale features
        df_scaled = scaler.transform(df)

        # Make prediction
        prediction = model.predict(df_scaled)

        # Result formatting and recommendation
        advice_list = [
            "Try to incorporate more fruits and vegetables into your diet!",
            "Consider regular physical activity, such as walking or cycling.",
            "Don't forget to drink plenty of water every day.",
            "A balanced diet and regular check-ups can help maintain your health."
        ]
        if prediction[0] == 1:
            result = "At risk of cancer"
            medical_advice = "It is recommended to visit a healthcare professional for further screening and advice on lifestyle changes to reduce cancer risk. " + advice_list[0]
        else:
            result = "Healthy"
            medical_advice = "You are in good health! Keep maintaining your healthy lifestyle. " + advice_list[1]

        return {"prediction": result, "advice": medical_advice}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))