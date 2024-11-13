
# POSTING ORDER

curl --location --request GET "https://j84ue9ihj8.execute-api.us-east-1.amazonaws.com/Prod/orders" \
--header "Authorization: $ID_TOKEN" \
--header "Content-Type: application/json"



export USERS_STACK_NAME=ws-serverless-patterns-users-WSS70A43TQYT
export ORDERS_STACK_NAME=ws-serverless-patterns-orders

aws cloudformation describe-stacks --stack-name $USERS_STACK_NAME --query "Stacks[0].Outputs"
aws cloudformation describe-stacks --stack-name $ORDERS_STACK_NAME --query "Stacks[0].Outputs"

export ID_TOKEN=$(aws cognito-idp initiate-auth \
  --auth-flow USER_PASSWORD_AUTH \
  --client-id 1ik5fe6udgf3e39sqm0pmp42o1 \
  --auth-parameters USERNAME="",PASSWORD='' \
  --query 'AuthenticationResult.IdToken' --output text)
echo $ID_TOKEN


