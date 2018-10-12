import json
from .validator import JsonStructureValidator

from builtins import isinstance


class BaseJsonModel(object):
    '''
    Базовая модель json
    '''
    
    BASE_TYPE = lambda v = None: v
    "тип поля"
    
    _jsons = '',
    "строка json из которой собирается объект"
    
    _json = {}
    "json с указанными типами полей"
    
    _structure = {}
    "описание структуры json"
    
    _validator = None
    "валидатор модели"
    
    _errors = []
    "сообщения ошибок валидаторов"
    
    _name = None
    "имя модели в структуре json"
    
    def __init__(self, jsonObject = None, validator = None, validatorArgs = None):
        
        self.loadJson(jsonObject)
        
        if validator is not None and issubclass(validator, JsonStructureValidator):
            if validatorArgs is None:
                validatorArgs = {}
            
            self.setValidator(validator(self._json, **validatorArgs))
        
        self._afterInit()
    
    def validate(self):
        "метод запускает валидатор"
        result = True
        
        if self._validator != None:
            v = self._validator()
            v.run(self._json)
            result = v.isValid()
            self._errors = v.getMessages()
        return result
    
    def getValidator(self):
        " получить валидатор"
        return self._validator
    
    def setValidator(self, validator):
        "установить валидатор"
        self.validator = validator
    
    def hasErrors(self):
        "есть ли ошибки валидатора"
        return len(self._errors) > 0
    
    def getErrors(self):
        "получить список ошибок"
        return self._errors
    
    def setJson(self, json):
        "установить json"
        self._json = json
    
    def loadJson(self, jsonData):
        "собрать объект с json"
        mapping = self._structure
        
        if jsonData is None:
            if '_self' in mapping:
                jsonData = mapping['_self']()
            else:
                jsonData = {self.__getName(): {}}
                for f in list(mapping):
                    jsonData[self.__getName()][f] = mapping[f]()
                self._json = jsonData[self.__getName()]
                return
        
        if isinstance(jsonData, BaseJsonModel):
            self._json = jsonData
        
        if '_self' in mapping:
            ob = jsonData
            
            if self._name in jsonData:
                ob = jsonData[self._name]
            
            self._json = mapping['_self'](ob)
            
            return
        if self.__getName() == None:
            raise Exception('pdlease define model name {}'.format(self.__class__))
        if self.__getName() in jsonData:
            data = {}
            income = jsonData[self.__getName()]
            
            for d in list(income):
                for m in list(mapping):
                    if m == d:
                        data[d] = mapping[m](income[d])
            
            self._json = data
        
        
        else:
            raise Exception("model {} not found in json ".format(self.__getName()))
    
    def getJson(self):
        "получить json"
        result = self._json.copy()
        
        if '_self' in self._structure:
            
            for k, v in enumerate(result):
                if isinstance(v, BaseJsonModel):
                    result[k] = v.getJson()
            return self._structure['_self'](result)
        
        for p in list(self._json):
            if isinstance(self._json[p], BaseJsonModel):
                result[p] = self._json[p].getJson()
        
        return {self._name: result}
        
    def __getName(self):
        " получаем имя модели"
        return self._name
    
    def __setName(self, name):
        "установить имя модели"
        self._name = name
    
    def _afterInit(self):
        "метод выполняется после инициализации"
        pass


class BaseResponse(BaseJsonModel):
    "базовая модель ответа "
    CODE_MODEL_ERROR = 'model_error'
    "код ответа ошибка модели"
    
    CODE_VALIDATION_ERROR = 'validation_error'
    "код ответа ошибка валидации"
    
    CODE_OK = 'OK'
    "код ответа ок"
    
    _name = "response"
    "имя модели"
    
    _json = {
        "code":    None,
        "message": None
    }
    "базовая структура модели ответа"
    
    _structure = {
        "code":    int,
        "message": str
    }
    "описание структуры модели"
    
    def __init__(self, code: str, message: str):
        self._json['code'] = code
        self._json['message'] = message
    
    def getCode(self):
        "получить код ответа"
        return self._json['code']
    
    def setCode(self, code):
        "установить код ответа"
        self._json['code'] = code
    
    def getMessage(self):
        "получить сообщение ответа"
        return self._json['message']
    
    def setMessage(self, message):
        "установить сообщение ответа"
        self._json['message'] = message


class ModelErrorResponse(BaseResponse):
    "модель ответа ошибки моделей"
    _json = {
        "code":   None,
        "models": None
    }
    "структура ответа"
    
    _structure = {
        "code":   int,
        "models": list
    }
    "описание структуры объекта"
    
    _name = "error"
    "имя модели структуры в json"
    
    _models = []
    "список моделей ошибки которых будут отображены"
    
    def __init__(self, models):
        self._json['code'] = self.CODE_VALIDATION_ERROR
        self._models = models
    
    def setModel(self, models):
        " установить модель "
        self._models = models
    
    def getModels(self):
        " получть модели "
        return self._models
    
    def getJson(self):
        "получить объект в dict"
        models = self._models.copy()
        self._json['models'] = []
        
        for m in models:
            self._json['models'].append({m._name: m.getErrors()})
        
        return super().getJson()
