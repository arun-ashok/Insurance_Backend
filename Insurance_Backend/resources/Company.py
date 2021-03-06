from flask_restful import Resource
from flask import make_response, request,jsonify
from mongoengine.errors import DoesNotExist, ValidationError
from Insurance_Backend.documents import user_doc as Users_Doc
from Insurance_Backend.documents import company_doc as Company_Doc
from Insurance_Backend.documents import form_doc as Form_Doc
import smtplib
from email.mime.text import MIMEText
from Insurance_Backend.resources.token_jwt import encode_auth_token,decode_auth_token


class Company(Resource):

    def post(self):
        request_body = request.get_json()
        print(request_body)
        email = request_body['email']
        company_name = request_body['company_name']
        if('token' in request_body):
            token=request_body['token']
            if(not token==''):
                email1=decode_auth_token(token)
                print(email1)
                print(email)
                if(not email1==email):
                    return make_response("Error Occured Try Again", 404)
            else:
               return make_response("Error Occured Try Again", 404)
        else:
            return make_response("Error Occured Try Again", 404)
        try :
            company1 = Form_Doc.Form.objects(email=email,b1=company_name).first()

            if(company1):
                return make_response(jsonify({'message':'Company already exists','success':0}),401)

            else:
                company1=Company_Doc.Company(email=email,company_name=company_name)
                if('company_name' in request_body):
                    company1.first_name = request_body['company_name']
                if('contact_person' in request_body):
                    company1.contact_person = request_body['contact_person']
                if('company_email' in request_body):
                    company1.company_email = request_body['company_email']
                    company_email=request_body['company_email']
                if('company_address' in request_body):
                    company1.address = request_body['company_address']
                if('products_required' in request_body):
                    company1.products_required = request_body['products_required']
                company1.save()
        except ValidationError as ve:
            print(str(ve))
            return make_response(jsonify({'message': "Validation error occured:" + str(ve), 'success': 0}), 404)
        except Exception as e:
            print(str(e))
            return make_response(jsonify({'message': "Error occured:" + str(e), 'success': 0}), 404)
        try:
            link="http://localhost:4200/fillform?email="+email+"&company_email="+company_email
            #msg = MIMEText('<h1>{link}</h2>','html')
            msg=MIMEText(link)
            msg['Subject']='Company Form'
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.login("perilwisea@gmail.com", "perilwise1234")
            message="http//localhost5000/perilwise/v1/companyform?email=arunashok22@gmail.com"
            server.sendmail("perilwisea@gmail.com", company_email, msg.as_string())
            server.quit()
        except Exception as e:
            print("Error while sending email")
            print(str(e))
            return make_response(jsonify({'message': "Company Added but email not sent!!",'success':0}),401)
        return make_response(jsonify({'message': "Company Added!!!", 'success': 1}), 200)




    def delete(self):
        email = request.args.get('email')
        company_email=request.args.get('company_email')
        print("email",email)
        print("c_email",company_email)

        company1 = Form_Doc.Form.objects(email=email, company_email=company_email).first()
        print(company1)
        if(company1):
            Form_Doc.Form.objects(email=email,company_email=company_email).delete()
            return make_response(jsonify({'message': "Company Added!!!", 'success': 1}), 200)
        else:
            print("Comapny not found error")
            return make_response(jsonify({'message': "Company Not Found!!!", 'success': 0}), 501)

        #except Exception as e:
        #    return make_response(jsonify({'message': "Company couldnt be deleted", 'success': 0}), 401)




