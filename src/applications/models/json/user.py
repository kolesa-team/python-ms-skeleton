from src.lib.application.models.json.model import BaseJsonModel
from src.lib.application.models.json.validator import (JsonStructureValidator, JsonDataValidator, IntValidator,
                                                       StringValidator, FloatValidator)


class UserExpenseValidator(JsonStructureValidator):
    ''' Валидатор записи траты пользователя '''
    _must = [
        "id",
        "date",
        "sum",
    ]
    '''обязательные поля'''
    
    _optional = [
        'comment'
    ]
    "поля опциональные"
    
    _validators = {
        "id":      [{"class": IntValidator, "args": {}}],
        "date":    [{"class": StringValidator, "args": {}}],
        "sum":     [{"class": FloatValidator, "args": {}}],
        "comment": [{"class": StringValidator, "args": {}}],
    }
    "валидаторы полей"


class UserExpensesValidator(JsonDataValidator):
    ''' валидатор поля растрат пользователя '''
    
    def _validate(self, data):
        '''
        метод выполняет валидацию всех объектов растрат пользователя
        
        :param data: данные поля
        :return: bool
        '''
        
        j = data.getJson() if isinstance(data, BaseJsonModel) else data
        
        if type(j) is list:
            for rec in j:
                expense = UserExpense(rec)
                
                if expense.validate() == False:
                    self.appendMessages(expense.getErrors())
                    
                    return False
            
            return True
        
        else:
            self.appendMessage("expenses value type isn't list")
            
            return False


class UserValidator(JsonStructureValidator):
    ''' Валидатор json структуры пользователя'''
    
    _must = [
        'id',
        "name",
        "surname",
        "age",
    ]
    ''' обязательные поля структуры '''
    
    _optional = [
        "phone",
        "friends",
        "address",
        "expenses"
    ]
    ''' обязательные поля структуры '''
    
    _validators = {
        "id":       [{"class": IntValidator, "args": {}}],
        "name":     [{"class": StringValidator, "args": {}}],
        "surname":  [{"class": StringValidator, "args": {}}],
        "address":  [{"class": StringValidator, "args": {}}],
        "expenses": [{"class": UserExpensesValidator, "args": {}}],
        "age":      [{"class": IntValidator, "args": {}}],
    }
    ''' валидаторы полей '''


class UserExpense(BaseJsonModel):
    ''' модель записи траты пользователя '''
    _name = 'expense'
    "имя модели в json структуре"
    
    _structure = {
        "id":      BaseJsonModel.BASE_TYPE,
        "date":    BaseJsonModel.BASE_TYPE,  # дата в формате yyyy-mm-dd hh:mm:ss
        "sum":     BaseJsonModel.BASE_TYPE,  # сумма в float
        "comment": BaseJsonModel.BASE_TYPE  # комментарий к трате
    }
    ''' структура json объекта растраты '''
    
    _validator = UserExpenseValidator
    ''' Валидатор структуры '''
    
    def getId(self):
        "получить id записи"
        return self._json['id']
    
    def setId(self, id):
        " установить id записи"
        self._json['id'] = id
    
    def getDate(self):
        return self._json['date']
    
    def setDate(self, date):
        self._json['date'] = date
    
    def getSum(self):
        return self._json['sum']
    
    def setSum(self, sum):
        self._json['sum'] = sum
        
    def getComment(self):
        return self._json['comment']

    def setComment(self, comment):
        self._json['comment'] = comment


class UserExpenses(BaseJsonModel):
    ''' модель растрат пользователя'''
    _name = "expenses"
    "имя модели в json структуре"
    
    _json = []
    ''' данные объекта '''
    
    _structure = {
        "_self": list
    }
    " структура объекта "
    
    _validator = UserExpensesValidator
    ''' валидатор данных '''
    
    def addOne(self, expense: UserExpense):
        ''' добавляем трату пользователя '''
        self._json.append(expense)
    
    def addMany(self,expenses):pass
        # if isinstance(expenses,UserExpenses):
        
    def getAll(self):
        ''' поулчаем растраты пользователя '''
        return self._json


class UserModel(BaseJsonModel):
    '''
    демо модель пользователя
    '''
    _name = 'user'
    "имя модели в json структуре"
    
    _structure = {
        "id":       BaseJsonModel.BASE_TYPE,  # id пользователя
        "name":     BaseJsonModel.BASE_TYPE,  # имя пользователя
        "surname":  BaseJsonModel.BASE_TYPE,  # фамилия пользователя
        "age":      BaseJsonModel.BASE_TYPE,  # возраст пользователя
        "address":  BaseJsonModel.BASE_TYPE,  # адрес пользователя
        "phone":    BaseJsonModel.BASE_TYPE,  # телефон пользователя
        "expenses": UserExpenses,  # расстраты пользователя
        "friends":  list  # список id друзей пользователя
    }
    "структура модели с описанием типов полей"
    
    _validator = UserValidator
    "Класс структурного валидатора"
    
    def getId(self):
        '''получить id пользователя'''
        return self._json['id']
    
    def setId(self, id):
        ''' установить id пользователя '''
        self._json['id'] = id
    
    def getName(self):
        ''' получить имя пользователя '''
        return self._json['name']
    
    def setName(self, name):
        ''' установить имя пользователя '''
        self._json['name'] = name
    
    def getSurname(self):
        ''' получить фамилию пользователя '''
        return self._json['surname']
    
    def setSurname(self, surname):
        ''' установить фамилию пользователя '''
        self._json['surname'] = surname
    
    def getAge(self):
        ''' получить возраст пользователя '''
        return self._json['age']
    
    def setAge(self, age):
        ''' установить возраст пользователя '''
        self._json['age'] = age
    
    def getAddress(self):
        ''' получить адрес пользователя '''
        return self._json['address']
    
    def setAddress(self, address):
        ''' установить адрес пользователя '''
        self._json['address'] = address
    
    def getPhone(self):
        ''' получить телефон пользователя '''
        return self._json['phone']
    
    def setPhone(self, phone):
        ''' установить телефон пользователя '''
        self._json['phone'] = phone
    
    def getExpenses(self)->UserExpenses:
        ''' получить растраты пользователя '''
        return self._json['expenses']
    
    def setExpenses(self, expenses:UserExpenses):
        ''' установить растраты пользователя '''
        self._json['expenses'] = expenses
    
    def addExpense(self,expense):
        self._json['expenses'].addOne(expense)
    
    
    def getFriends(self):
        ''' получить список id друзей пользователя '''
        return self._json['friends']
    
    def setFriends(self, friends):
        ''' установить список id друзей пользователя '''
        self._json['friends'] = friends
