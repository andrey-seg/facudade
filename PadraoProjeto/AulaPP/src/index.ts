interface IPagamento{
    valor: number;
};

class PagamentoPix implements IPagamento{
    constructor(public valor: number){}
}

class PagamentoCartao implements IPagamento{
    constructor(public valor: number){}
}

interface ProcessarPagamento{
    criarPagamento(valor: number): IPagamento;
}

class ProcessarPagamentoPix implements ProcessarPagamento{
    criarPagamento(valor: number): IPagamento {
        return new PagamentoPix(valor);
    };
};

class ProcessarPagamentoCartao implements ProcessarPagamento{
    criarPagamento(valor: number): IPagamento {
        return new PagamentoCartao(valor);
    };
};

class Pedido {

    constructor(private processador: ProcessarPagamento){}
    finalizar(valor: number) {

        const pagamento = this.processador.criarPagamento(valor)
 }
}