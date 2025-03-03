# Ingestion service

 # Ingestion Service Flow Diagram
 

```{mermaid} 
sequenceDiagram
    %% Client/User on the left
    box MistyRose Client
        participant Client as Client/User
    end

    box Thistle Producer
        participant API as Producer API
        participant Validator as Producer Validator
        participant Publisher as Producer RabbitMQ Publisher
    end

    box LightGoldenRodYellow RabbitMQ Queue
        participant RabbitMQ as RabbitMQ Queue
    end

    box HoneyDew Consumer
        participant Consumer as Worker Consumer/Listener
        participant Processor as Worker Processor
    end

    box AliceBlue Query Service
        participant QueryService as Query Service
    end

    box Wheat Graph Database
        participant GraphDB as Graph Database
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
    
    %% Worker service processes the message
    RabbitMQ->>Consumer: 5. Consume message
    activate Consumer
    Consumer->>Processor: 6. Process data
    activate Processor
    
    %% Processing steps
    Processor->>Processor: 7. Add provenance metadata
    
    %% Acknowledge message
    Processor-->>Consumer: Processing complete, provenance attached

    %% Send to query service
    Consumer->>QueryService: 8. Send processed data
    activate QueryService
    
    %% Store in database
    QueryService->>GraphDB: 9. Store in graph database
    activate GraphDB
    GraphDB-->>QueryService: Storage confirmation
    deactivate GraphDB
    
    QueryService-->>Processor: Processing confirmation
    deactivate QueryService
    
    %% Acknowledge message
    Processor-->>Consumer: Processing complete
    deactivate Processor
    Consumer->>RabbitMQ: 10. Acknowledge message
    deactivate Consumer 
```