## 📚 Learning Roadmap

QueueSense is being developed phase-by-phase as a personal learning project. Each phase introduces new backend concepts while adding a real feature to the application.

### Phase 1 — FastAPI Foundations
**Status:** ✅ Completed

**Tasks:**
- FastAPI project setup
- Basic GET endpoints
- Path parameters
- Query parameters
- Request bodies
- Pydantic schemas
- API testing with Swagger

**Learning:**
- FastAPI fundamentals
- REST API concepts
- HTTP methods and status codes
- Request/response handling
- Pydantic validation
- API documentation with Swagger


### Phase 2 — PostgreSQL & SQLAlchemy
**Status:** ✅ Completed

**Tasks:**
- PostgreSQL setup
- Neon database connection
- SQLAlchemy setup
- Database sessions
- ORM models
- Alembic setup
- Database migrations

**Learning:**
- PostgreSQL fundamentals
- Relational database concepts
- SQLAlchemy ORM
- Models and tables
- Foreign keys
- Database sessions
- Alembic migrations
- Schema evolution


### Phase 3 — Organization → Branch → Service
**Status:** ✅ Completed

**Tasks:**
- Organization model
- Branch model
- Service model
- Relationships between entities
- Organization APIs
- Branch APIs
- Service APIs
- Filtering services by branch

**Learning:**
- Database relationships
- One-to-many relationships
- Foreign keys
- SQLAlchemy relationships
- API route organization
- Resource validation
- Modular FastAPI routes


### Phase 4 — Customer Queue Flow
**Status:** ✅ Completed

**Tasks:**
- Queue → Service relationship
- Queue creation
- Queue discovery
- Joining a queue
- Token generation
- Queue position
- Leaving/cancelling a queue
- Customer queue status

**Learning:**
- Queue-based business logic
- Database querying with SQLAlchemy
- Transactions
- Row locking
- Preventing duplicate queue entries
- Counting records with `func.count()`
- Combining multiple query conditions
- State-based business rules


### Phase 5 — Queue Logic
**Status:** ✅ Completed

**Tasks:**
- Call next customer
- Serve customer
- Skip / mark no-show
- Pause queue
- Resume queue
- Close queue

**Learning:**
- State transitions
- Queue lifecycle
- Customer lifecycle
- Business-rule validation
- Resource state management
- Separating queue state from customer state
- Designing backend operations around real-world workflows


### Phase 6 — ETA & Queue Statistics
**Status:** 🟡 In Progress

**Tasks:**
- Service session tracking
- Average service time
- ETA / estimated wait time
- Queue statistics
- Customer-facing queue summary
- Improve ETA using service history

**Learning:**
- Timestamp handling
- Service session modelling
- SQL aggregation
- `func.avg()`
- `func.count()`
- SQL joins
- Historical data
- ETA calculations
- Queue analytics


### Phase 7 — Authentication & Authorization
**Status:** ⬜ Upcoming

**Tasks:**
- User model
- Registration
- Login
- Password hashing
- JWT authentication
- Token validation
- Role-based access control
- Customer / Staff / Admin permissions

**Learning:**
- Authentication vs authorization
- Password security
- JWT
- Access tokens
- Role-based access control
- Protected routes
- Secure identity handling


### Phase 8 — Staff Dashboard Backend
**Status:** ⬜ Upcoming

**Tasks:**
- Staff queue dashboard APIs
- Current customer
- Waiting customers
- Queue controls
- Staff actions
- Queue operational data

**Learning:**
- Role-specific APIs
- Dashboard backend design
- Complex business logic
- Efficient database queries
- Backend-driven workflows


### Phase 9 — Real-Time Queue Updates
**Status:** ⬜ Upcoming

**Tasks:**
- WebSocket setup
- Real-time queue updates
- Customer screen updates
- Staff action broadcasting
- Live token changes

**Learning:**
- WebSockets
- Real-time communication
- Connection management
- Event-driven backend logic
- Synchronizing frontend and backend state


### Phase 10 — History & Notifications
**Status:** ⬜ Upcoming

**Tasks:**
- Customer queue history
- Service history
- Notifications
- Queue status notifications
- Notification tracking

**Learning:**
- Historical data modelling
- Notification architecture
- Background processing concepts
- Event-based workflows


### Phase 11 — Admin Backend & Analytics
**Status:** ⬜ Upcoming

**Tasks:**
- Organization management
- Branch management
- Service management
- Queue management
- Staff management
- Admin statistics
- Operational analytics

**Learning:**
- Admin systems
- Multi-level resource management
- Aggregation queries
- Analytics APIs
- Role-based backend architecture


### Phase 12 — Security & Production Polish
**Status:** ⬜ Upcoming

**Tasks:**
- Input validation
- Authorization checks
- Secure error handling
- CORS configuration
- Environment variables
- Rate limiting where appropriate
- Transaction safety
- API security review

**Learning:**
- Backend security
- Secure API design
- Secrets management
- Defensive programming
- Production considerations
- Error handling


### Phase 13 — React Frontend & API Integration
**Status:** ⬜ Upcoming

**Tasks:**
- React application setup
- API integration
- Authentication integration
- Customer flows
- Staff flows
- Admin flows

**Learning:**
- Connecting React with FastAPI
- API clients
- Frontend/backend communication
- Authentication from the frontend
- Full-stack architecture


### Phase 14 — Customer UI & Live Queue
**Status:** ⬜ Upcoming

**Tasks:**
- Customer dashboard
- Browse services
- Join queue
- Queue status
- Position tracking
- ETA display
- Real-time updates

**Learning:**
- Real-time frontend state
- WebSocket integration
- User experience for queue systems
- Handling API and live data together


### Phase 15 — Staff & Admin Dashboard UI
**Status:** ⬜ Upcoming

**Tasks:**
- Staff dashboard
- Queue controls
- Customer management
- Admin dashboard
- Statistics and analytics UI

**Learning:**
- Dashboard architecture
- Role-based UI
- Data visualization
- Complex frontend state management
- Full-stack feature integration


### Phase 16 — Testing, Deployment & Final Polish
**Status:** ⬜ Upcoming

**Tasks:**
- API testing
- Edge-case testing
- Security testing
- Backend deployment
- Frontend deployment
- Production configuration
- Documentation
- Final project cleanup

**Learning:**
- Testing strategies
- Deployment
- Production debugging
- Environment configuration
- API reliability
- Software project completion
