# Ingestion service

{numref}`brainkb_intestion_architecture_figure`  illustrates the architecture of the ingestion service, which follows the producer-consumer pattern and leverages RabbitMQ for scalable data ingestion. The service is composed of two main components: (i) the producer and (ii) the consumer.
The producer component exposes API endpoints (see {numref}`brainkb_ingestion_service_api_endpoints`) that allow clients or users to ingest data. Currently, it supports the ingestion of KGs represented in JSON-LD and Turtle formats. Users can ingest raw JSON-LD data as well as upload files, either individually or in batches. At present, the ingestion of other file types, such as PDF, text, and JSON, has been disabled due to the incomplete implementation of the required functionalities.



```{figure} images/ingest.png
:name: brainkb_intestion_architecture_figure
Architecture of Ingestion Service.
```

```{figure} images/api_endpoints_ingestion_service.png
:name: brainkb_ingestion_service_api_endpoints
Currently Enabled API Endpoints.
```




## Sequence Diagram
 
```{mermaid}
sequenceDiagram
    %% Client/User on the left
    box MistyRose Client
        participant Client as Client/User
    end

    box Thistle Producer
        participant API as Producer API
        participant Validator as  Shared.py
        participant Publisher as RabbitMQ Publisher
    end

    box LightGoldenRodYellow RabbitMQ 
        participant RabbitMQ as RabbitMQ Queue
    end

    %% Client submits data
    Client->>API: 1. POST data (JSON-LD, TTL, etc.)
    activate API
    
    %% Producer service validates and publishes
    API->>Validator: 2. Validate data format
    activate Validator
    Validator-->>API: Validation result
    deactivate Validator
    
    alt is valid data
        API->>Publisher: 3. Format data for publishing
        activate Publisher
        Publisher->>RabbitMQ: 4. Publish message to queue
        Publisher-->>API: Publish confirmation
        deactivate Publisher
        API-->>Client: 200 OK Response
    else invalid data
        API-->>Client: 400 Bad Request
    end
    deactivate API
```

```{mermaid} 
sequenceDiagram
    %% Client/User on the left
    
    box LightGoldenRodYellow RabbitMQ 
        participant RabbitMQ as RabbitMQ Queue
    end

    box HoneyDew Consumer
        participant Consumer as Listener
        participant Processor as  Shared.py
    end

    box AliceBlue Query Service
        participant QueryService as Query Service
    end

    box Wheat Graph Database
        participant GraphDB as Graph Database
    end
 
      
    
    %% Worker service processes the message
    RabbitMQ->>Consumer: 1. Consume message
    activate Consumer
    Consumer->>Processor: 2. Process data
    activate Processor
    
    %% Processing steps
    Processor->>Processor: 3. Add provenance metadata
    
    %% Acknowledge message
    Processor-->>Consumer: Processing complete, provenance attached

    %% Send to query service
    Consumer->>QueryService: 4. Send processed data
    activate QueryService
    
    %% Store in database
    QueryService->>GraphDB: 5. Store in graph database
    activate GraphDB
    GraphDB-->>QueryService: Storage confirmation
    deactivate GraphDB
    
    QueryService-->>Processor: Processing confirmation
    deactivate QueryService
    
    %% Acknowledge message
    Processor-->>Consumer: Processing complete
    deactivate Processor
    Consumer-->>RabbitMQ: 6. Acknowledge message
    deactivate Consumer 
```