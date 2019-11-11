import json, requests, os
import sys
import smtplib as s
from email import encoders
from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart
from dictor import dictor
import requests



def main():
    banner()
    opcao_menu = int(input('QUAL OPCAO? '))
    
    if (opcao_menu == 1): 
        os.system('clear') or None
        validarPagamento()
    if (opcao_menu == 2): 
        os.system('clear') or None
        validarPagamento()
    if (opcao_menu == 3): 
        os.system('clear') or None
        gerarAdmToken()        

    
def validarPagamento():
    access_token = raw_input('Qual Access_token (Pode inserir ADM TOKEN)? ')
    payment = raw_input('Qual Pagamento? ')


    try:
        # PEDIDO COM MUITOS ITENS
     # response = requests.get("https://api.mercadopago.com/v1/payments/5378897871?access_token=*******102503613")
    # PEDIDO COM ITENS FALTANDO
        response = requests.get("https://api.mercadopago.com/v1/payments/"+str(payment)+"?access_token="+str(access_token))
    # print response.status_code
     comments = json.loads(response.content)

    except Exception as e:
        os.system('clear') or None
        print "                         VERIFIQUE OS DADOS INSERIDOS" 
        main()   
    


    # VERIFICAR SE TEM ADDITIONAL_INFO
    print "_______________________"
    print "#### ADDITIONAL_INFO ####"
    if (validarAdditional(comments)):
        print "Additional_info |  OK  |"
        additional_info = "OK"
    else:
        # print "Payer -         | ERROR|"
        additional_info = "ERROR"
    print "#### PAYER ####"    
    
    # VERIFICAR SE O PAYER ESTA CORRETO
    if (validarPayer(comments)):
        print "Payer -         |  OK  |"
        payer = "OK"
    else:
        payer = "ERROR"
    
    # VERIFICAR QUAL STATUS ESTA O MODO BINARIO
    if (validarBinary(comments)):
        print "Binary_mode -   | TRUE |"
        binary = "TRUE"
    else:
        print "Binary_mode -   | FALSE|"
        binary = "FALSE"
    # VERIFICAR SE HOUVE HIGH_RISK
    if (validarStatus(comments)):
        print "Status -   | HIGH_RISK |"
        status = "HIGH_RISK"
    else:
        print "Status -        |  OK  |"        
        status = "OK"
 
    if (pagamentoFluxo(comments)):
        print "PNF -           | TRUE |"
        pnf = "TRUE"
    else:
        print "PNF -           | FALSE|"   
        pnf = "FALSE"
    print "_______________________"

    opcao_menu = int(input('DESEJA ENVIAR POR EMAIL (1 - SIM / 2 - NAO)? '))
    
    if (opcao_menu == 1): 
        textoToString = resultadoToString(additional_info,payer,binary,status,pnf,str(comments["id"]))
        email = raw_input('Qual email?')
        enviarEmail(email, textoToString)

    if (opcao_menu == 2): 
        os.system('clear') or None
        main()
    else:
        os.system('clear') or None
        print "Opcao invalida"
        main()

def resultadoToString(additional_info,payer,binary,status,pnf,id):
    inicioHtml = ""
    texto = "ID - "+ id +"\n\n\nAdditional_info - " + additional_info + "\nPayer -  " + payer + "\nBinary_mode - " + binary + "\nStatus - " + status + "\nPNF - " + pnf
   
    return texto
    
def gerarAdmToken():
    os.system('clear') or None
    usuarioRede = raw_input('Usuario Rede: ')
    senhaRede  = raw_input('Senha Rede: ')
    d = {'grant_type': "password", 'client_id': 601, 'client_secret': 'ysqWSflbtbZl2vXkFLd4NWvNAzTq6b7X', 'username': usuarioRede, 'password': senhaRede}   
    response = requests.post("https://api.mercadolibre.com/admin/oauth/token", data=d)
    comments = json.loads(response.content)
    os.system('clear') or None
    print comments['access_token']
    main()     

def validarAdditional(comments):

    additional_info = False
    # print comments["additional_info"]
    
    if len(comments["additional_info"])!=0:
            additional_info = True
                 # VALIDAR ITEMS
            if len(comments["additional_info"]["items"])!=0:
                reload(sys)
                sys.setdefaultencoding( "latin-1" )
                
                if str(dictor(comments, "additional_info.items.0.category_id"))=="None":
                    print "- Faltando additional_info.items.category_id"
                    additional_info = False
                if str(dictor(comments, "additional_info.items.0.description"))=="None":
                    print "- Faltando additional_info.items.description"
                    additional_info = False
                if str(dictor(comments, "additional_info.items.0.id"))=="None":
                    print "- Faltando additional_info.items.id"  
                    additional_info = False
                if str(dictor(comments, "additional_info.items.0.picture_url"))=="None":
                    print "- Faltando additional_info.items.picture_url"
                    additional_info = False
                if str(dictor(comments, "additional_info.items.0.quantity"))=="None":
                    print "- Faltando additional_info.items.quantity"
                    additional_info = False
                if str(dictor(comments, "additional_info.items.0.title"))=="None":
                    print "- Faltando additional_info.items.title"
                    additional_info = False
                if str(dictor(comments, "additional_info.items.0.unit_price"))=="None":
                    print "- Faltando additional_info.items.unit_price"
                    additional_info = False
            else:
                print "- Faltando additional_info.items"
                additional_info = False
                
                # VALIDAR PAYER
            if  len(comments["additional_info"]["payer"])!=0:
                
                if len(comments["additional_info"]["payer"]["first_name"])!=0:
                    print "- Faltando additional_info.payer.first_name"                    
                if len(comments["additional_info"]["payer"]["last_name"])!=0:       
                    print "- Faltando additional_info.payer.last_name"                    
                if len(comments["additional_info"]["payer"]["phone"])!=0:       
                    print "- Faltando additional_info.payer.phone"
                if len(comments["additional_info"]["payer"]["address"])!=0:       
                     if str(dictor(comments, "additional_info.payer.street_name"))=="None":
                        print "- Faltando additional_info.payer.street_name"
                        additional_info = False
                     if str(dictor(comments, "additional_info.payer.street_number"))=="None":
                        print "- Faltando additional_info.payer.street_number"
                        additional_info = False
                     if str(dictor(comments, "additional_info.payer.zip_code"))=="None":
                        print "- Faltando additional_info.payer.zip_code"
                        additional_info = False
                else:
                    print "- Faltando additional_info.payer.address"
            else:
                print "- Faltando additional_info.payer"
                additional_info = False
                # VALIDAR SHIPMENT
            if  len(comments["additional_info"]["shipments"])!=0:
                if  len(comments["additional_info"]["shipments"]["receiver_address"])==0:
                    print "- Faltando additional_info.shipments"    
                    additional_info = False
            else:
                print "- Faltando additional_info.shipments"
                additional_info = False        



    else:
        print "- Faltando additional_info"
    
    return additional_info

def validarPayer(comments):

    payer = False
    # print comments["payer"]
    
    if len(comments["payer"])!=0:
        payer = True
        if str(dictor(comments, "payer.email"))=="None":
            payer = False
            print "- Faltando payer.email"
        if str(dictor(comments, "payer.first_name"))=="None":
            payer = False
            print "- Faltando payer.first_name"
        if len(comments["payer"]["identification"])!=0:
            if str(dictor(comments, "payer.identification.number"))=="None":
                payer = False
                print "- Faltando payer.identification.number"
            if str(dictor(comments, "payer.identification.type"))=="None":
                payer = False
                print "- Faltando payer.identification.type"
    
    return payer

def validarBinary(comments):

    binary = False
    # print comments["payer"]
    
    if (comments["binary_mode"])==True:
            binary = True
    
    
    return binary           

def validarStatus(comments):
    status = False
    # print comments["payer"]
    
    if (comments["status"])=="rejected":
            if (comments["status_detail"])=="cc_rejected_high_risk":
                status = True
    
    
    
    
    return status   

def pagamentoFluxo(comments):

    pagamento = False
    
    
    if (comments["money_release_schema"])=="payment_in_flow":
            pagamento = True
    
    
    return pagamento   

# ENVIO EMAIL PT 1
def enviarEmail(email, comments):
    email_user = "enganatroxaolx@gmail.com"
    email_pass = "tartaruga123"

    validade,conn = validarEmail(email_user, email_pass)
    print comments
    if validade == True:
        executarEnvio(email_user,conn,comments,email)

    else:
        print "Erro ao validar conta de envio de email"
        main()    

# ENVIO EMAIL PT 2
def executarEnvio(email_user,conn,comments,destinatario):

    FROM = email_user
    TO = destinatario

    #Escreve o e-mail
    SUBJECT = "Validacao de pagamento"
    
    text = str(comments)

    #Formata a mensagem nos padroes de envio SMTP
    
  
    

    #Envia o E-mail
    
    message = MIMEMultipart()
    message['From'] = FROM
    message['To'] = TO
    message['Subject'] = SUBJECT
    message.attach(MIMEText(text, 'plain'))
    email = message.as_string()

    try:
        conn.sendmail(FROM, TO, email)
        os.system('clear') or None
        print 'Email enviado com sucesso!'
        main()
    except:
        print 'Fail...'
        sys.exit()

#VALIDA O LOGIN E SENHA
def validarEmail(email_user, email_pass):
    try:
        conn = s.SMTP('smtp.gmail.com', 587)
        conn.starttls()
        conn.ehlo
        conn.login(email_user, email_pass)
        return True,conn

    except:
        print 'FALHA NA CONEXAO'
        print '1 - VERIFIQUE SEU USUARIO E SENHA'
        print '2 - CERTIFIQUE-SE DE QUE HABILITOU OS APLICATIVOS MENOS SEGUROS'
        print 'URL: https://www.google.com/settings/security/lesssecureapps'
        return False




def banner():
    print """
 ---| MENU HOMOLOGATOR  |-----------------------------------------------------------------------------------
|                                                                                                           |
|   1 - VALIDAR UM PAGAMENTO                                                                                |
|   2 - CONSULTAR COLLECTOR DE UM PAGAMENTO (Nao implementado)                                              |
|   3 - GERAR ADM TOKEN                                                                                     |
|   ATENCIOSAMENTE: MSS_IT                                                                                  |
 -----------------------------------------------------------------------------------------------------------
 """
    return True

main()