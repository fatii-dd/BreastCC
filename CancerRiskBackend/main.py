from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class CancerRiskData(BaseModel):
    BRCA: int
    BMI_NEW_GROUP: int
    AGE_NEW_GROUP: int
    PROVINCE_NEW_GROUP: int
    GENDER_N: int

@app.post("/predict/")
def predict_cancer_risk(data: CancerRiskData):
    # การประมวลผล (สามารถใส่โมเดลของคุณได้ที่นี่)
    # ตัวอย่างง่าย ๆ คืนค่า BRCA เป็นคำตอบ
    result = {"cancer_risk": "high" if data.BRCA == 1 else "low"}
    return result