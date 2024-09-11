import React, { useState } from 'react';
import './css.css'; // import CSS file

const PredictionForm = () => {
    const [formData, setFormData] = useState({
        brca: '',
        weight: '',
        height: '',
        age: '',
        province: '',
        gender: ''
    });
    const [result, setResult] = useState('');
    // const [advice, setAdvice] = useState('');

    const handleChange = (e) => {
        const { id, value } = e.target;
        setFormData({
            ...formData,
            [id]: value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
    
        // ส่งข้อมูลไปยัง FastAPI backend
        try {
            const response = await fetch('http://127.0.0.1:8000/predict/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    BRCA: [formData.brca],
                    BMI_GROUP: { weight: parseFloat(formData.weight), height: parseFloat(formData.height) },
                    AGE_GROUP: parseInt(formData.age),
                    PROVINCE_GROUP: [formData.province],
                    GENDER_N: formData.gender
                })
            });
    
            const result = await response.json();
            
            // แสดงผลการทำนายและคำแนะนำผ่าน JSX
            setResult(
                <div>
                    <h3 style={{ color: result.prediction === 'At risk of cancer' ? 'red' : 'green' }}>
                        Prediction: {result.prediction}
                    </h3>
                    <p style={{ fontSize: '1.2em', fontFamily: 'Arial, sans-serif' }}>
                        {/* Advice: {result.advice} */}
                    
                    </p>
                </div>
            );
        } catch (error) {
            console.error('Error:', error);
            setResult(<p style={{ color: 'red' }}>An error occurred.</p>);
        }
    };

    return (
        <div className="container">
            <h1>Predict Breast Cancer Risk</h1>
            <form id="predictionForm" onSubmit={handleSubmit}>
                <label htmlFor="brca">BRCA Result:</label>
                <select id="brca" value={formData.brca} onChange={handleChange} required>
                    <option value="negative">Negative</option>
                    <option value="positive">Positive</option>
                </select>

                <label htmlFor="weight">Weight (kg):</label>
                <input
                    type="number"
                    id="weight"
                    step="0.1"
                    value={formData.weight}
                    onChange={handleChange}
                    required
                />

                <label htmlFor="height">Height (m):</label>
                <input
                    type="number"
                    id="height"
                    step="0.01"
                    value={formData.height}
                    onChange={handleChange}
                    required
                />

                <label htmlFor="age">Age:</label>
                <input
                    type="number"
                    id="age"
                    value={formData.age}
                    onChange={handleChange}
                    required
                />

                <label htmlFor="province">Province:</label>
                <select id="province" value={formData.province} onChange={handleChange} required>
                    <option value="ยะลา">ยะลา</option>
                    <option value="ปัตตานี">ปัตตานี</option>
                    <option value="นราธิวาส">นราธิวาส</option>
                    <option value="สงขลา">สงขลา</option>
                    <option value="สตูล">สตูล</option>
                    <option value="พังงา">พังงา</option>
                    <option value="พัทลุง">พัทลุง</option>
                    <option value="อื่นๆ">อื่นๆ</option>
                </select>

                <label htmlFor="gender">Gender:</label>
                <select id="gender" value={formData.gender} onChange={handleChange} required>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                </select>

                <button type="submit">Predict</button>
            </form>

            <h2 id="result">{result}</h2>
        </div>
    );
};

export default PredictionForm;