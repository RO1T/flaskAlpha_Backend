from flask_restful import reqparse

registerParser = reqparse.RequestParser()
registerParser.add_argument("login", type=str)
registerParser.add_argument("password", type=str)
registerParser.add_argument("role", type=str)

loginParser = reqparse.RequestParser()
loginParser.add_argument("login", type=str)
loginParser.add_argument("password", type=str)

profileParser = reqparse.RequestParser()
profileParser.add_argument("username", type=str)
profileParser.add_argument("description", type=str)

surveyCreateParser = reqparse.RequestParser()
surveyCreateParser.add_argument("title", type=str)
surveyCreateParser.add_argument("description", type=str)
surveyCreateParser.add_argument("pages", type=dict, action="append")

answerSendParser = reqparse.RequestParser()
answerSendParser.add_argument("answers", type="append")