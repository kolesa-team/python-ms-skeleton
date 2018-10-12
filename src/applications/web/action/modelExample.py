import json

from src.lib.application.webApp.action import Action
from src.applications.models.json.user import UserModel, UserExpenses, UserExpense
from src.lib.application.models.json.model import BaseResponse,ModelErrorResponse

class ModelExampleAction(Action):
    '''
    демонстрационный экшен
    
    показывает как распарсить модель из запроса обектами
    провалидировать, изменить запись и выдать объектами ответ
    
    пример запроса
    {
        "user":{
            "id" : 15868,
            "name" : "Ари",
            "age": 33,
            "surname" : "Левитан",
            "phone" : "+77026202048",
            "address" : "Куйбышева 42",
            "expenses" : [
                    {
                        "expense" : {
                            "id" : 1586,
                            "date" : "2018-02-12 12:22:48",
                            "sum" : 5000.54,
                            "comment" : "оплата баланс на телефон"
                        }
                    },{
                        "expense" : {
                            "id" : 5698,
                            "date" : "2018-02-12 12:48:12",
                            "sum" : 2000.00,
                            "comment" : "обед"
                        }
                    },{
                        "expense" : {
                            "id" : 5244,
                            "date" : "2018-02-12 13:34:55",
                            "sum" : 500.00,
                            "comment" : "такси"
                        }
                    }
                ],
            "friends" : [
                    1245,
                    6589,
                    2659
                ]
        }
    }
    '''
    def get(self):
        self.write((BaseResponse(BaseResponse.CODE_OK,"use post method for this action")).getJson())
    
    def post(self):
        try:
            user = UserModel(json.loads(self.request.body))
            
            if user.validate() == False:
                error = ModelErrorResponse([user])
                self.write(error.getJson())
                return
            
            expense = UserExpense()
            
            expense.setId(12567)
            expense.setDate("2018-10-09 12:29:53")
            expense.setSum(12000.00)
            expense.setComment("тренажерка")
            
            user.addExpense(expense)
            
            self.write((BaseResponse(BaseResponse.CODE_OK,"record processed successful")).getJson())
            
        except Exception as e:
            self.write((BaseResponse(BaseResponse.CODE_MODEL_ERROR,str(e))).getJson())
            
