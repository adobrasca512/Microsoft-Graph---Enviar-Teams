import asyncio
from msgraph import *
from msgraph.generated.models.chat import *
from msgraph.generated.models.chat_type import ChatType
from msgraph import GraphServiceClient
from msgraph.generated.models.chat_message import ChatMessage
from msgraph.generated.models.item_body import ItemBody
from msgraph.generated.models.conversation_member import *
from msgraph.generated.models.aad_user_conversation_member import *
from azure.identity import UsernamePasswordCredential

async def main():
    CLIENT_ID = 'client_id'
    TENANT_ID = 'tenant_id'
    USERNAME = 'example@cincuentenario.com'
    PASSWORD = 'contrasena'
    SCOPE = ["https://graph.microsoft.com/.default"]  # The required permissions
    CLIENT_SECRET = 'client_secret'
    # Authenticate using username and password
    credentials = UsernamePasswordCredential(tenant_id=TENANT_ID,client_secret=CLIENT_SECRET,
    client_id=CLIENT_ID,
    username=USERNAME,
    password=PASSWORD)
    
    graph_client = GraphServiceClient(credentials, SCOPE)

    # Create chat request body
    request_body = Chat(
        chat_type=ChatType.OneOnOne,
        members=[
            AadUserConversationMember(
                odata_type="#microsoft.graph.aadUserConversationMember",
                roles=["owner"],
                additional_data={
                    "user@odata.bind": "https://graph.microsoft.com/v1.0/users('example1@cincuentenario.com')",
                }
            ),
            AadUserConversationMember(
                odata_type="#microsoft.graph.aadUserConversationMember",
                roles=["owner"],
                additional_data={
                    "user@odata.bind": "https://graph.microsoft.com/v1.0/users('example2@cincuentenario.com')",
                }
            ),
        ],
    )

    # Create chat
    chat_created = await graph_client.chats.post(request_body)

    # Create message request body
    request_body = ChatMessage(
        body=ItemBody(
            content="Hello world",
        ),
    )

    # Send message to the created chat
    result = await graph_client.chats.by_chat_id(chat_created.id).messages.post(request_body)

    return result

# Run the main function asynchronously
asyncio.run(main())
