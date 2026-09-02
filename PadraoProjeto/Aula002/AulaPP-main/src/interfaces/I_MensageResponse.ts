import { I_ApiResponse } from "./I_ApiResponse";

export interface I_MensageResponse<T>{

    findById(id: string): Promise<I_ApiResponse<T>>;
    findAll(): Promise<I_ApiResponse<T>>;
    save(entity: T): Promise<I_ApiResponse<T>>;
    delete(id: string): Promise<I_ApiResponse<T>>;
}