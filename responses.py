def create_response(client, message):
    reponse_list = [
        {"role": "therapist",
         "content": "You are a therapist. Read messages and determine the emotion felt"},
         {"role": "user",
          "content": message}
    ]

    response = client.chat.completions.create(
        model = "gpt-3.5-turbo-0125",
        messages = reponse_list,
        tools=[{"type": "code_interpreter"}],
        temperature = 0
    )

    return response.choices[0].message.content