# Microservices Architecture - Skill

Create production-ready microservices architectures with Docker, proper service communication, and deployment strategies.

## Usage

```
/microservices <project-name> [options]
```

## Invocation Examples

- `/microservices bella-italia --services="frontend,backend,voice" --database="postgresql"`
- `/microservices e-commerce --scale="high" --pattern="event-driven"`
- `/microservices saas-app --gateway="nginx" --monitoring="prometheus"`

## Instructions for Claude

When this skill is invoked, follow this comprehensive process to create a microservices architecture:

---

## PHASE 1: DISCOVERY & REQUIREMENTS ANALYSIS

### 1.1 Project Understanding

Ask the user these critical questions using AskUserQuestion:

**Business Requirements:**
- What is the primary purpose of the system?
- What are the main features/capabilities needed?
- Who are the end users?
- What's the expected scale? (users, requests/sec, data volume)

**Technical Requirements:**
- What services/components have you identified so far?
- Any preferred technology stack? (Node.js, Python, Go, etc.)
- Database preferences? (PostgreSQL, MongoDB, Redis, etc.)
- Any existing systems to integrate with?

**Infrastructure Requirements:**
- Development environment setup? (local Docker Compose)
- Production deployment target? (Docker Swarm, Kubernetes, cloud provider)
- Budget constraints?
- Team size and expertise level?

**Non-Functional Requirements:**
- Performance requirements (latency, throughput)
- Availability requirements (uptime %)
- Security requirements (compliance, data sensitivity)
- Monitoring and observability needs

---

## PHASE 2: ARCHITECTURE DESIGN PRINCIPLES

Apply these fundamental microservices principles:

### 2.1 Service Design Principles

**Single Responsibility Principle:**
- Each service should do ONE thing well
- Clear boundaries and responsibilities
- Avoid "god services" that do everything

**Database Per Service:**
- Each service owns its data
- No direct database access between services
- Communicate through APIs only
- Allows independent scaling and technology choices

**Decentralized Data Management:**
- Services can use different databases (polyglot persistence)
- Handle data consistency with patterns (Saga, Event Sourcing)
- Accept eventual consistency where appropriate

**Design for Failure:**
- Assume services will fail
- Implement retry logic with exponential backoff
- Circuit breakers for dependent services
- Graceful degradation
- Health checks and automatic recovery

**Loose Coupling, High Cohesion:**
- Minimal dependencies between services
- Changes in one service shouldn't require changes in others
- Use well-defined contracts (OpenAPI, gRPC schemas)

### 2.2 Service Identification Strategy

**Decomposition Patterns:**

1. **By Business Capability:**
   - User Management Service
   - Order Service
   - Payment Service
   - Notification Service

2. **By Subdomain (Domain-Driven Design):**
   - Bounded contexts define service boundaries
   - Each subdomain becomes a service
   - Example: User Authentication vs User Profile (different contexts)

3. **By Data Ownership:**
   - Services that need exclusive write access to data
   - Read replicas can be shared

**Anti-Patterns to Avoid:**
- Too fine-grained (nano-services) = network overhead
- Too coarse-grained = defeats purpose of microservices
- Chatty services = poor performance
- Distributed monolith = tight coupling with microservices structure

---

## PHASE 3: SERVICE COMMUNICATION PATTERNS

### 3.1 Synchronous Communication

**REST APIs (HTTP/JSON):**
```yaml
Use When:
  - Simple CRUD operations
  - Public-facing APIs
  - Browser/mobile clients
  - Team familiar with REST

Pros:
  - Easy to understand and debug
  - Wide tooling support
  - Cacheable with HTTP
  
Cons:
  - Higher latency than gRPC
  - Coupling through endpoints
```

**Example REST Service Communication:**
```javascript
// Frontend → Backend API
fetch('http://backend-service:3001/api/reservations', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ date, time, partySize })
})
```

**gRPC (Protocol Buffers):**
```yaml
Use When:
  - Internal service-to-service communication
  - High performance needed
  - Strong typing required
  - Polyglot environment

Pros:
  - Fast (binary protocol)
  - Strong contracts (.proto files)
  - Bi-directional streaming
  - Code generation
  
Cons:
  - More complex setup
  - Not browser-friendly (needs proxy)
  - Steeper learning curve
```

### 3.2 Asynchronous Communication

**Message Queues (RabbitMQ, Redis Streams):**
```yaml
Use When:
  - Fire-and-forget operations
  - Decoupling producers/consumers
  - Load leveling
  - Guaranteed delivery needed

Patterns:
  - Work Queues: Task distribution
  - Pub/Sub: Event broadcasting
  - Request/Reply: Async RPC
```

**Example Message Queue:**
```javascript
// Voice Service → Backend (reservation created event)
await channel.publish('events', 'reservation.created', Buffer.from(JSON.stringify({
  id: reservation.id,
  customer: { name, phone },
  details: { date, time, partySize }
})));

// Backend subscribes and processes
channel.consume('reservation.created', (msg) => {
  const reservation = JSON.parse(msg.content);
  await saveToDatabase(reservation);
  await sendConfirmationEmail(reservation);
});
```

**Event Streaming (Kafka, Redis):**
```yaml
Use When:
  - Event sourcing architecture
  - Real-time data pipelines
  - High throughput needed
  - Event replay capability

Pros:
  - Scalable
  - Durable event log
  - Replay capability
  - Decoupling
```

### 3.3 Service Discovery

**Static Discovery (Docker Compose DNS):**
```yaml
services:
  frontend:
    # Can access backend via: http://backend:3001
  backend:
    # Can access voice via: http://voice-service:5000
```

**Dynamic Discovery (Consul, Eureka):**
- Services register themselves
- Health checks
- Load balancing
- Used in production Kubernetes

---

## PHASE 4: DOCKER & CONTAINERIZATION STRATEGY

### 4.1 Dockerfile Best Practices

**Multi-Stage Builds:**
```dockerfile
# Example: Node.js service optimized Dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:20-alpine AS runner
WORKDIR /app
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 appuser
COPY --from=builder --chown=appuser:nodejs /app/node_modules ./node_modules
COPY --chown=appuser:nodejs . .
USER appuser
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD node healthcheck.js || exit 1
CMD ["node", "server.js"]
```

**Security Principles:**
- Use minimal base images (alpine, distroless)
- Don't run as root (create app user)
- Multi-stage builds to reduce image size
- Scan images for vulnerabilities
- Use specific version tags (not :latest)

### 4.2 Docker Compose Architecture

**Network Strategy:**
```yaml
networks:
  frontend-network:
    driver: bridge
  backend-network:
    driver: bridge
    internal: true  # No external access
  
services:
  nginx:
    networks:
      - frontend-network
  
  frontend:
    networks:
      - frontend-network
      - backend-network
  
  backend:
    networks:
      - backend-network
  
  database:
    networks:
      - backend-network
```

**Volume Strategy:**
```yaml
volumes:
  # Named volumes for data persistence
  postgres-data:
  redis-data:
  
services:
  postgres:
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./init-scripts:/docker-entrypoint-initdb.d:ro
```

**Health Checks:**
```yaml
services:
  backend:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3001/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

---

## PHASE 5: API GATEWAY PATTERN

### 5.1 Why API Gateway?

**Benefits:**
- Single entry point for clients
- Request routing to services
- Load balancing
- Authentication/Authorization
- Rate limiting
- Request/Response transformation
- SSL termination
- API versioning

### 5.2 Nginx as API Gateway

**Example Configuration:**
```nginx
upstream frontend {
    server frontend:3000;
}

upstream backend {
    server backend:3001;
}

upstream voice-service {
    server voice:5000;
}

server {
    listen 80;
    server_name example.com;

    # Frontend
    location / {
        proxy_pass http://frontend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Backend API
    location /api/ {
        proxy_pass http://backend/;
        proxy_set_header Host $host;
        
        # CORS headers
        add_header Access-Control-Allow-Origin *;
        
        # Rate limiting
        limit_req zone=api_limit burst=10 nodelay;
    }

    # Voice Service (WebSocket support)
    location /voice/ {
        proxy_pass http://voice-service/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### 5.3 Alternative Gateways

- **Kong**: Plugin-based, feature-rich
- **Traefik**: Auto-discovery, Let's Encrypt
- **AWS API Gateway**: Managed service
- **Azure API Management**: Enterprise features

---

## PHASE 6: DATA MANAGEMENT STRATEGIES

### 6.1 Database Patterns

**Pattern 1: Database Per Service (Recommended)**
```yaml
services:
  user-service:
    depends_on:
      - user-db
  user-db:
    image: postgres:16
    environment:
      POSTGRES_DB: users
  
  order-service:
    depends_on:
      - order-db
  order-db:
    image: postgres:16
    environment:
      POSTGRES_DB: orders
```

**Pattern 2: Shared Database (Use Sparingly)**
- Only for tightly coupled services
- Simpler but creates coupling
- Harder to scale independently

### 6.2 Data Consistency Patterns

**Saga Pattern (Distributed Transactions):**
```
Order Created → Reserve Inventory → Process Payment → Confirm Order
                      ↓ (fail)            ↓ (fail)
                Cancel Order ← Release Inventory
```

**Event Sourcing:**
- Store events, not current state
- Rebuild state by replaying events
- Full audit trail
- Time travel debugging

**CQRS (Command Query Responsibility Segregation):**
- Separate read and write models
- Optimize each independently
- Read replicas for queries
- Write to master database

### 6.3 Caching Strategy

**Redis for Caching:**
```yaml
services:
  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis-data:/data
  
  backend:
    environment:
      REDIS_URL: redis://redis:6379
```

**Caching Patterns:**
- **Cache-Aside**: Check cache → miss → load from DB → store in cache
- **Write-Through**: Write to cache and DB simultaneously
- **Write-Behind**: Write to cache → async write to DB

---

## PHASE 7: OBSERVABILITY & MONITORING

### 7.1 The Three Pillars

**1. Logging (Centralized Logs)**
```yaml
services:
  loki:
    image: grafana/loki:latest
  
  promtail:
    image: grafana/promtail:latest
    volumes:
      - /var/log:/var/log
  
  backend:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

**2. Metrics (Prometheus + Grafana)**
```yaml
services:
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
  
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=secret
```

**3. Tracing (Jaeger, Zipkin)**
```yaml
services:
  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686"  # UI
      - "6831:6831/udp"  # Agent
```

### 7.2 Health Check Endpoints

**Liveness vs Readiness:**
```javascript
// backend/health.js
app.get('/health/live', (req, res) => {
  // Is the service alive? (basic check)
  res.status(200).json({ status: 'ok' });
});

app.get('/health/ready', async (req, res) => {
  // Is the service ready to accept traffic?
  try {
    await db.query('SELECT 1');
    await redis.ping();
    res.status(200).json({ 
      status: 'ready',
      database: 'connected',
      redis: 'connected'
    });
  } catch (error) {
    res.status(503).json({ 
      status: 'not ready',
      error: error.message 
    });
  }
});
```

---

## PHASE 8: SECURITY BEST PRACTICES

### 8.1 Secret Management

**Using Docker Secrets (Swarm) or Environment Variables:**
```yaml
services:
  backend:
    environment:
      DATABASE_URL: ${DATABASE_URL}
      JWT_SECRET: ${JWT_SECRET}
      ELEVENLABS_KEY: ${ELEVENLABS_KEY}
    secrets:
      - db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

**For Production:**
- Vault (HashiCorp)
- AWS Secrets Manager
- Azure Key Vault
- Kubernetes Secrets

### 8.2 Network Security

**Principle of Least Privilege:**
```yaml
networks:
  public:
    driver: bridge
  
  private:
    driver: bridge
    internal: true  # No internet access

services:
  # Public-facing
  nginx:
    networks:
      - public
      - private
  
  # Internal only
  database:
    networks:
      - private
```

### 8.3 Authentication & Authorization

**JWT Token Flow:**
```
Client → API Gateway (validate JWT) → Service
                ↓ (invalid)
              401 Unauthorized
```

**Service-to-Service Auth:**
- API Keys
- Mutual TLS (mTLS)
- Service mesh (Istio)

---

## PHASE 9: DEPLOYMENT STRATEGIES

### 9.1 Local Development (Docker Compose)

**Development Override:**
```yaml
# docker-compose.yml (base)
services:
  backend:
    image: backend:latest
    environment:
      NODE_ENV: production

# docker-compose.override.yml (local dev)
services:
  backend:
    build: ./backend
    volumes:
      - ./backend:/app
      - /app/node_modules
    environment:
      NODE_ENV: development
    command: npm run dev
```

### 9.2 Production Deployment

**Option 1: Docker Swarm**
```bash
docker stack deploy -c docker-compose.prod.yml myapp
```

**Option 2: Kubernetes**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: backend:v1.2.3
        ports:
        - containerPort: 3001
```

**Option 3: Cloud Managed**
- AWS ECS/Fargate
- Google Cloud Run
- Azure Container Instances

### 9.3 CI/CD Pipeline

**GitHub Actions Example:**
```yaml
name: Build and Deploy

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build images
        run: docker-compose build
      
      - name: Run tests
        run: docker-compose run backend npm test
      
      - name: Push to registry
        run: |
          docker tag backend:latest registry.example.com/backend:${{ github.sha }}
          docker push registry.example.com/backend:${{ github.sha }}
      
      - name: Deploy to production
        run: kubectl set image deployment/backend backend=registry.example.com/backend:${{ github.sha }}
```

---

## PHASE 10: IMPLEMENTATION WORKFLOW

### 10.1 Step-by-Step Process

**Step 1: Define Services**
- List all services identified
- Define responsibilities for each
- Identify data ownership

**Step 2: Design Communication**
- Which services talk to which?
- Synchronous or asynchronous?
- API contracts (OpenAPI, gRPC schemas)

**Step 3: Create Project Structure**
```
project-root/
├── docker-compose.yml
├── docker-compose.override.yml (dev)
├── docker-compose.prod.yml (production)
├── .env.example
├── nginx/
│   └── nginx.conf
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   └── src/
├── backend/
│   ├── Dockerfile
│   ├── package.json
│   └── src/
├── voice-service/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
└── monitoring/
    ├── prometheus.yml
    └── grafana/
```

**Step 4: Implement Each Service**
- Start with backend/API services
- Implement health checks
- Add logging
- Write tests

**Step 5: Create Dockerfiles**
- Multi-stage builds
- Security hardening
- Health checks

**Step 6: Configure Docker Compose**
- Define all services
- Set up networks
- Configure volumes
- Add health checks
- Set resource limits

**Step 7: Add API Gateway**
- Nginx configuration
- Routing rules
- SSL/TLS setup
- Rate limiting

**Step 8: Implement Monitoring**
- Prometheus metrics
- Grafana dashboards
- Log aggregation
- Distributed tracing

**Step 9: Testing**
- Unit tests per service
- Integration tests
- Load testing
- Chaos engineering (optional)

**Step 10: Documentation**
- API documentation (OpenAPI/Swagger)
- Architecture diagrams
- Deployment instructions
- Runbooks for operations

---

## PHASE 11: COMMON ARCHITECTURES & TEMPLATES

### 11.1 E-Commerce Microservices

```yaml
services:
  # Frontend
  web-ui:
    build: ./web-ui
    ports: ["80:3000"]
  
  # API Gateway
  api-gateway:
    image: nginx
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
  
  # Services
  user-service:
    build: ./user-service
  
  product-service:
    build: ./product-service
  
  order-service:
    build: ./order-service
  
  payment-service:
    build: ./payment-service
  
  notification-service:
    build: ./notification-service
  
  # Databases
  user-db:
    image: postgres:16
  
  product-db:
    image: postgres:16
  
  order-db:
    image: postgres:16
  
  # Message Broker
  rabbitmq:
    image: rabbitmq:management
  
  # Cache
  redis:
    image: redis:7-alpine
```

### 11.2 SaaS Application

```yaml
services:
  frontend:
    build: ./frontend
  
  auth-service:
    build: ./auth-service
  
  tenant-service:
    build: ./tenant-service
  
  billing-service:
    build: ./billing-service
  
  analytics-service:
    build: ./analytics-service
  
  notification-service:
    build: ./notification-service
  
  postgres:
    image: postgres:16
  
  redis:
    image: redis:7-alpine
  
  elasticsearch:
    image: elasticsearch:8.11.0
```

---

## PHASE 12: TROUBLESHOOTING GUIDE

### Common Issues

**1. Services Can't Communicate**
```bash
# Check network connectivity
docker-compose exec backend ping frontend

# Check DNS resolution
docker-compose exec backend nslookup frontend

# Inspect networks
docker network ls
docker network inspect project_backend-network
```

**2. Service Won't Start**
```bash
# View logs
docker-compose logs backend

# Check health status
docker-compose ps

# Inspect container
docker-compose exec backend sh
```

**3. Performance Issues**
```bash
# Monitor resource usage
docker stats

# Check service health
curl http://localhost:3001/health

# View metrics
curl http://localhost:9090/metrics
```

---

## SUCCESS CRITERIA

A microservices architecture is well-designed when:

✅ **Each service has a clear, single responsibility**
✅ **Services are independently deployable**
✅ **Communication patterns are well-defined**
✅ **Data ownership is clear (database per service)**
✅ **Health checks are implemented**
✅ **Monitoring and logging are in place**
✅ **Security best practices followed**
✅ **Documentation is comprehensive**
✅ **Can scale services independently**
✅ **Failure of one service doesn't cascade**

---

## ANTI-PATTERNS TO AVOID

❌ **Distributed Monolith**: Microservices that all must be deployed together
❌ **Chatty Services**: Too many network calls between services
❌ **Shared Database**: Multiple services writing to same tables
❌ **No API Gateway**: Clients calling services directly
❌ **Missing Health Checks**: Can't detect service failures
❌ **No Monitoring**: Flying blind in production
❌ **Tight Coupling**: Changes in one service break others
❌ **Nano-services**: Too granular, overhead exceeds benefits

---

## FINAL NOTES

**Start Simple, Grow Complex:**
- Begin with a monolith if appropriate
- Extract services as needed
- Don't over-engineer early

**Team Considerations:**
- Microservices require DevOps maturity
- Need proper tooling and processes
- Communication overhead increases

**When NOT to Use Microservices:**
- Small team (< 5 people)
- Simple application
- No need for independent scaling
- Limited DevOps capability

**Best Practices:**
- Automate everything (CI/CD, testing, deployment)
- Monitor relentlessly
- Document thoroughly
- Design for failure
- Keep services small and focused

---

When implementing, always explain your architectural decisions and trade-offs to the user.
