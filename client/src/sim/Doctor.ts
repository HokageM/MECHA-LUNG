import { PatientData } from "./PatientData";

export interface Doctor {
    id: number;
    user_name: string;
    hashed_password: string;
    patient_data: PatientData[];
}
