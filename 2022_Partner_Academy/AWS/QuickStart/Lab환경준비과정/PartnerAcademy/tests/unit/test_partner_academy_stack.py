import aws_cdk as core
import aws_cdk.assertions as assertions

from partner_academy.partner_academy_stack import PartnerAcademyStack

# example tests. To run these tests, uncomment this file along with the example
# resource in partner_academy/partner_academy_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = PartnerAcademyStack(app, "partner-academy")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
