import { IsNumber, IsString } from "class-validator";

export class CreateCertificadoDto {

    @IsString()
    titulo: string;

    @IsString()
    descriacao: string;

    @IsNumber()
    cargaHoraria: number;

    @IsString()
    dataInicio: string;

    @IsString()
    dataFim: string;

    @IsString()
    instituicao: string;
}
