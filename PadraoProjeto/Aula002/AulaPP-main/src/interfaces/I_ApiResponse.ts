export interface I_ApiResponse<T>{
    success: boolean,
    data?: <T>,
    error?: string;
}