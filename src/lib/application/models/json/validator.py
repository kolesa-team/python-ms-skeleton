
class JsonBaseValidator(object):
    ''' базовый валидатор '''
    
    _data = None
    "данные для валидации"
    
    _pass = None
    "пройдена ли валидация ?"
    
    _kwargs = None
    " аргументы передаваемые в конструктор объекта"
    
    _errorMessages = []
    "сообщения об ошибках"
    
    def __init__(self, **kwargs):
        self._kwargs = kwargs
    
    def _validate(self, data) -> bool:
        ''' метод валидации, который нужно реализовывать дочерним объектам '''
        self._errorMessages = []
        raise Exception('implement _validate method')
    
    def getMessages(self):
        " вернуть сообщения"
        return self._errorMessages
    
    def setMessages(self, messages):
        " установить сообщения"
        self._errorMessages = messages
    
    def appendMessage(self, message):
        " добавить сообщение об ошибках "
        self._errorMessages.append(message)
    
    def appendMessages(self, messages):
        " добавить массив сообщений "
        for m in messages:
            self._errorMessages.append(m)
    
    def isValid(self):
        " прошел ли тест "
        return self._pass
    
    def getModelName(self):
        " получить имя модели "
        return type(self).__name__
    
    def run(self, data):
        " запуск валидатора "
        self.data = data
        self._errorMessages = []
        
        if self._validate(self.data):
            self._pass = True
        else:
            self._pass = False


class JsonDataValidator(JsonBaseValidator):
    "валидатор данных"
    
    pass


class JsonStructureValidator(JsonBaseValidator):
    "валидатор структуры json"
    
    VALIDATOR_NOT_ALLOWED = 'NotAllowed'
    " ключ валидатора 'поле запрещено' "
    
    VALIDATOR_MUST_EXIST = 'MustExist'
    " ключ валидатора 'поле должно существовать' "
    
    _json = {}
    " данные для валидации "
    
    _must = []
    " список обязательных полей в структуре "
    
    _optional = []
    " список опциональных полей в структуре"
    
    _validators = {}
    '''
    маппинг валидаторов полей { 'поле': [{'class': ValidatorClass, 'args' : {} }] }
    где в class присваивается класс (не объект) валидатора
    в args передаются kwargs для конструктора этого валидатора
    
    на одно поле можно добавлять несколько валидаторов
    '''
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def _validate(self, data: list):
        " метод запускает наличие полей must, optional и запускает валидаторы каждого поля "
        
        self._json = data
        
        if len(self._optional) > 0 or len(self._must) > 0:
            for p in list(data):
                if p not in self._optional and p not in self._must:
                    error = {
                        p: [{"validator": self.VALIDATOR_NOT_ALLOWED, "messages": ['{} key is not allowed'.format(p)]}]}
                    self.appendMessage(error)
        
        if len(self._must) > 0:
            
            for m in self._must:
                if m not in data:
                    error = {m: [{"validator": self.VALIDATOR_MUST_EXIST, "messages": ['{} key not set'.format(m)]}]}
                    self.appendMessage(error)
        
        if len(self._validators) > 0:
            error = {}
            for p in list(data):
                
                if p in self._validators:
                    for v in self._validators[p]:
                        validator = v['class'](**v['args'])
                        validator.run(data[p])
                        
                        if validator.isValid() == False:
                            if p not in error:
                                error[p] = []
                            error[p].append(
                                {"validator": validator.getModelName(), "messages": validator.getMessages()})
            
            if len(error) > 0:
                self.appendMessage(error)
        
        return len(self.getMessages()) == 0


class IntValidator(JsonDataValidator):
    " валидатор типа int"
    
    def _validate(self, data):
        if type(data) == int:
            return True
        else:
            self.appendMessage('{} error, value is not an integer number'.format(self.getModelName()))
            return False


class FloatValidator(JsonDataValidator):
    " валидатор типа float "
    def _validate(self, data):
        if type(data) == float:
            return True
        else:
            self.appendMessage('{} error, value is not float number'.format(self.getModelName()))
            return False


class StringValidator(JsonDataValidator):
    " валидатор типа строки "
    def _validate(self, data):
        if type(data) == str:
            return True
        else:
            self.appendMessage('{} error, value is not string'.format(self.getModelName()))
            return False


class StringLengthValidator(JsonDataValidator):
    " вадидатор длинны строки"
    def _validate(self, data):
        
        length = 120
        
        if 'length' in self._kwargs:
            length = int(self._kwargs['length'])
        
        if (type(data) == str and len(data) > length) or (type(data) != str):
            self.appendMessage('{} error, string length is > {}'.format(self.getModelName(), length))
            return False
        
        return True