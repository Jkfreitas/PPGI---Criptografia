from random import getrandbits, randrange

#--- Gerador de primos ---
class GeradorNumeroPrimo:
    def __init__(self):
        self.numero_primo = self.gerar_numero_primo()

    def teste_miller_rabin(self,n, k=128):
        """ Testa se o número é primo
            Param:
                n - número testado
                k - número de testes
            return True if n is prime
        """
        if n < 6:  # valida alguns casos
            return [False, False, True, True, False, True][n]
        # Testa se n é par
        if n <= 1 or n % 2 == 0:
            return False
        # encontra r e s
        s = 0
        r = n - 1
        while r & 1 == 0:
            s += 1
            r //= 2
        # executa k testes
        for _ in range(k):
            a = randrange(2, n - 1)
            x = pow(a, r, n)
            if x != 1 and x != n - 1:
                j = 1
                while j < s and x != n - 1:
                    x = pow(x, 2, n)
                    if x == 1:
                        return False
                    j += 1
                if x != n - 1:
                    return False
        return True

    def tentativa_de_numero(self,length):
        """ Gera um número primo inteiro aleatório.
                retorna o número
        """
        # gera bits aleatórios
        self.numero_primo = getrandbits(length)
        # aplica uma mascara para determinar valor 1 para MSB e LSB
        self.numero_primo |= (1 << length - 1) | 1
        return self.numero_primo

    def gerar_numero_primo(self,length=5): #limita a 5bits por causa do processamento
        ''' Cria um número primo testado
            parâmetros: 
                length - tamanho em bits
        '''
        self.numero_primo  = 4 #falha proposital para start do loop while
        # Continua enquanto o teste falha
        while not self.teste_miller_rabin(self.numero_primo, 128):
            self.numero_primo  = self.tentativa_de_numero(length)
        return self.numero_primo 

#----- criptografia -----
class Criptografia(object):

    def criptografia(self, m, e, n):
        c = (m**e) % n
        return c

    def descriptografia(self, c, d, n):
        m = c**d % n
        return m

    def encripta_mensagem(self):
        print("--- INICIANDO O PROCESSO DE CRIPTOGRAFIA DA MENSAGEM --- ")
        s = input("\nDigite a mensagem: \t")
        print("\n")
        print('='*5 + ' Digite as chaves públicas: ' + '='*5)
        e = int(input("Chave e: \t"))
        n = int(input("Chave n: \t")) 
        enc = ''.join(chr(self.criptografia(ord(x), e, n)) for x in s)
        print('Texto Cifrado: ', enc, '\n')
        return enc
        
        
    def decripta_mensagem(self, s):
        self.s = s
        print("--- INICIANDO O PROCESSO DE DECRIPTOGRAFIA DA MENSAGEM --- ")
        print('='*5 + ' Digite as chaves privadas: ' + '='*5)
        d = int(input("Chave d: \t"))
        n = int(input("Chave n: \t")) 
        dec = ''.join(chr(self.descriptografia(ord(x), d, n)) for x in s)
        return print('Texto Simples: ', dec, '\n')

#--- Gerador de chaves ---
class Chaves(Criptografia):

    def __init__(self, p, q):
        self.p = p
        self.q = q

    def gerar_chaves(self):
        n=self.p*self.q
        phi=(self.p-1)*(self.q-1)  # Função totiente de Euler ou função Phi

        print("\nEscolha sua chave pública:\n")
        print(str(self.coprimos(phi)) + "\n") # calculo da chave pública mdc(phi(N), E) == 1
        e=int(input())
        
        d=self.inverso_modular(e,phi) # calculo da chave privada d*e = 1 mod(φ(n))
        return print("\nChaves públicas (e=" + str(e) + ", n=" + str(n) + ")" + "\nChaves privadas (d=" + str(d) + ", n=" + str(n) + ")\n")

    def mdc(self, a, b):
        while a != 0:
            a, b = b % a, a
        return b

    def inverso_modular(self, a, m): 
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        print('Não ha inverso modular para o bloco.\n')
        return None
        
    def coprimos(self, a):
        l = []
        for x in range(2, a): 
            if self.mdc(a, x) == 1 and self.inverso_modular(x,a) != None: #  MDC(φ(n), e) = 1
                l.append(x)
        for x in l:
            if x == self.inverso_modular(x,a):
                l.remove(x)
        return l

#-------- main -----------
p = GeradorNumeroPrimo()
numero_p = p.numero_primo
print('\nP :',str(numero_p))

q = GeradorNumeroPrimo()
numero_q = q.numero_primo
print('Q :',str(numero_q))

chaves = Chaves(numero_p, numero_q)
chaves.gerar_chaves()

encripta = chaves.encripta_mensagem()
chaves.decripta_mensagem(encripta)