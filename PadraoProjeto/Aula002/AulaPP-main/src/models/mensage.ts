import { MensageStatus } from "../enum/MensagesStatus";
import { I_Mensages } from "../interfaces/I_Mensages";

export class Mensage implements I_Mensages{

    private __id: string;
    private __name: string;
    private __cellphoneNumber: string;
    private __message: string;
    private __status: MensageStatus;

    constructor(id: string, name: string, cellphoneNumber: string, message: string, status: MensageStatus){

        this.__id = id;
        this.__name = name;
        this.__cellphoneNumber = cellphoneNumber;
        this.__message = message;
        this.__status = status;
    }

    sendMensage(mensage: string): string {
        return `Mensagem enviada para ${this.__cellphoneNumber}`;
    }

    receiveMessage(mensage: string): string {
        return `Voce recebeu uma mensagem => ${this.__message}`;
    }
}