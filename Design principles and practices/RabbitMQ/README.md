## Design
Diagram 1:
<br/>
![Diagram 1](https://github.com/PSS1998/Cloud-Software-and-Systems-Course/blob/8a365a46669cf88fb213ec4bcc51d021e151348b/Design%20principles%20and%20practices/RabbitMQ/exercise_instructions_diagrams_01.png)
<br/>
Diagram 2:
<br/>
![Diagram 2](https://github.com/PSS1998/Cloud-Software-and-Systems-Course/blob/8a365a46669cf88fb213ec4bcc51d021e151348b/Design%20principles%20and%20practices/RabbitMQ/exercise_instructions_diagrams_02.png)
<br/>
## Test
Run the following commands in script folder to test:<br/>
Start a worker with 
```
python3 run_worker.py --id "<worker-id>" --queue "<worker-id>_queue" -w "1"
```
<br/>

Start a customer app with 
```
python3 run_customer_app.py -c "<customer-id>"
```

<br/>

Generate ShoppingEvents through 
```
python3 produce_shopping_event.py -e "pick up" -c "<customer-id>" -t 5 and python3 produce_shopping_event.py -e "purchase" -c "<customer-id>" -t 10
```

<br/>
