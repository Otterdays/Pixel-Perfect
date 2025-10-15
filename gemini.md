# Project Context & Development Guidelines

## Purpose
This document provides persistent context for Gemini CLI to maintain architectural consistency, code quality, and development standards across this project.

---

## Project Architecture

### Core Principles
- **Modularity First**: Every component should be independently testable and replaceable
- **Explicit Dependencies**: No implicit coupling; all dependencies declared at module boundaries
- **Interface-Driven Design**: Define contracts before implementations
- **Separation of Concerns**: Business logic, data access, and presentation are strictly separated

### Directory Structure
```
/src
  /core           # Core business logic, framework-agnostic
  /infrastructure # External integrations (DB, APIs, file system)
  /interfaces     # API/UI layers
  /shared         # Utilities, types, constants used across modules
/tests            # Mirror src structure
/docs             # Architecture decisions, API specs
/scripts          # Build, deployment, utility scripts
```

### Module Boundaries
- **Core** may not import from infrastructure or interfaces
- **Infrastructure** implements interfaces defined in core
- **Interfaces** orchestrate core and infrastructure
- **Shared** contains only pure functions and types with zero side effects

---

## Code Standards

### Language & Framework Conventions
- Use TypeScript with strict mode enabled
- Prefer functional patterns over classes where appropriate
- Use async/await over raw Promises
- Error handling: explicit error types, never silent failures

### Naming Conventions
- **Files**: kebab-case (`user-repository.ts`)
- **Classes/Interfaces**: PascalCase (`UserRepository`)
- **Functions/Variables**: camelCase (`getUserById`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_RETRY_ATTEMPTS`)
- **Types**: PascalCase with descriptive suffixes (`UserDTO`, `CreateUserRequest`)

### Function Design
- Pure functions by default
- Single responsibility principle
- Max 50 lines per function (extract if longer)
- Explicit return types (no implicit `any`)
- Document complex logic with inline comments explaining *why*, not *what*

### Error Handling Pattern
```typescript
// Use Result types or explicit throws, never mixed
type Result<T, E = Error> = { success: true; data: T } | { success: false; error: E };

// Or throw with custom error types
class ValidationError extends Error {
  constructor(public field: string, message: string) {
    super(message);
  }
}
```

---

## Testing Requirements

### Coverage Expectations
- **Core modules**: 90%+ coverage
- **Infrastructure**: 80%+ coverage with integration tests
- **Interfaces**: E2E tests for critical paths

### Test Structure
```typescript
describe('FeatureName', () => {
  describe('specificFunction', () => {
    it('should handle expected case', () => { /* ... */ });
    it('should handle edge case X', () => { /* ... */ });
    it('should throw ValidationError when Y', () => { /* ... */ });
  });
});
```

### Test Principles
- Arrange-Act-Assert pattern
- One assertion per test (logical grouping)
- Test behavior, not implementation
- Mock external dependencies, test edge cases
- No test interdependencies

---

## Development Workflow

### Before Creating New Features
1. Define interfaces and types first
2. Write tests for expected behavior
3. Implement core logic
4. Add infrastructure integration
5. Connect through interface layer

### When Modifying Existing Code
1. Read related GEMINI.md context in that module
2. Check existing tests to understand intended behavior
3. Update tests first if changing behavior
4. Refactor with tests passing
5. Update documentation if interfaces change

### Code Review Checklist
- [ ] Follows naming conventions
- [ ] Respects module boundaries
- [ ] Includes tests with good coverage
- [ ] Handles errors explicitly
- [ ] Updates type definitions
- [ ] No hardcoded values (use config)
- [ ] Documented complex logic

---

## AI Assistant Guidelines

### When Generating Code
- **Ask Before Assuming**: If requirements are ambiguous, ask clarifying questions
- **Show Tradeoffs**: Explain architectural decisions and alternatives considered
- **Complete Implementations**: Don't use placeholders like `// TODO` unless specifically requested
- **Context Awareness**: Reference existing patterns in the codebase
- **Incremental Changes**: For large features, break into reviewable chunks

### When Refactoring
- Preserve existing behavior unless explicitly asked to change
- Update all related tests
- Identify ripple effects across modules
- Suggest migration paths for breaking changes

### When Debugging
- Reproduce the issue first
- Explain root cause
- Provide fix with test that would have caught it
- Suggest preventive measures

### Code Generation Priorities
1. **Correctness**: Works as specified
2. **Maintainability**: Clear, follows conventions
3. **Testability**: Easy to test in isolation
4. **Performance**: Efficient, but not at cost of clarity

---

## Common Patterns

### Dependency Injection
```typescript
// Define dependencies as interfaces
interface Logger {
  log(message: string): void;
}

// Inject through constructor
class UserService {
  constructor(
    private readonly repository: UserRepository,
    private readonly logger: Logger
  ) {}
}
```

### Configuration Management
```typescript
// Centralized, typed configuration
interface Config {
  database: {
    host: string;
    port: number;
  };
  api: {
    timeout: number;
    retries: number;
  };
}

// Load from environment with validation
const config = loadConfig();
```

### Async Operations
```typescript
// Prefer Promise.all for parallel operations
const [users, posts] = await Promise.all([
  fetchUsers(),
  fetchPosts()
]);

// Use for...of for sequential with await
for (const item of items) {
  await processItem(item);
}
```

---

## Anti-Patterns to Avoid

❌ **Global State**: Use dependency injection
❌ **Mixed Concerns**: Business logic in controllers/handlers
❌ **Implicit Dependencies**: Hidden coupling between modules
❌ **Magic Values**: Hardcoded strings/numbers without constants
❌ **God Objects**: Classes with too many responsibilities
❌ **Premature Optimization**: Profile before optimizing
❌ **Callback Hell**: Use async/await
❌ **Silent Failures**: Always handle errors explicitly

---

## Documentation Standards

### Code Comments
- Use JSDoc for public APIs
- Inline comments for complex algorithms
- Explain *why* decisions were made, not *what* code does

### Architecture Decisions
- Document in `/docs/adr/` using ADR format
- Include context, options considered, decision, consequences

### API Documentation
- OpenAPI/Swagger specs for REST APIs
- Include examples for common use cases
- Document error responses

---

## Performance Considerations

### Database Queries
- Use indexes on frequently queried fields
- Batch operations when possible
- Use pagination for large datasets
- Profile slow queries

### Caching Strategy
- Cache expensive computations
- Invalidate caches explicitly
- Document cache TTLs and invalidation rules

### Resource Management
- Close connections/streams explicitly
- Use connection pools
- Implement timeouts for external calls

---

## Security Guidelines

### Input Validation
- Validate all external input
- Use allowlists over denylists
- Sanitize before output

### Authentication & Authorization
- Never store credentials in code
- Use environment variables or secret management
- Implement principle of least privilege

### Dependencies
- Regular security audits
- Keep dependencies updated
- Review dependency licenses

---

## When to Break These Rules

These guidelines are strong defaults, not absolute laws. Break them when:
- Performance profiling shows a specific need
- External API constraints require different patterns
- Prototyping/experimenting with new approaches
- Legacy code integration requires compromise

**But**: Document why you're deviating and what the tradeoff is.

---

## Project-Specific Context

[Add project-specific details here:]
- Tech stack versions
- Critical business rules
- Domain-specific terminology
- Integration requirements
- Deployment environments
- Team conventions

---

*Last Updated: 2025-10-14*
*Review this document quarterly and after major architectural changes*