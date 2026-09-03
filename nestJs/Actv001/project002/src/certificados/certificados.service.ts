import { Injectable } from '@nestjs/common';
import { CreateCertificadoDto } from './dto/create-certificado.dto';
import { UpdateCertificadoDto } from './dto/update-certificado.dto';
import { Certificado } from './entities/certificado.entity';

@Injectable()
export class CertificadosService {

  private __certificados: Certificado[] = [];

  create(createCertificadoDto: CreateCertificadoDto): Certificado {
    
    const novoCertificado: Certificado = {

      id: this.__certificados.length + 1,
      ...createCertificadoDto,
    };
    this.__certificados.push(novoCertificado);
    return novoCertificado;
  }

  findAll(): Certificado[] {
    return this.__certificados;
  }

  findOne(id: number) {
    
    return this.__certificados.find((c) => c.id === id);

  }

  update(id: number, updateCertificadoDto: UpdateCertificadoDto): Certificado | undefined {
    
    const index = this.__certificados.findIndex((c) => c.id === id);
    if(index === -1) return undefined
  }

  remove(id: number) {
    return `This action removes a #${id} certificado`;
  }
}
