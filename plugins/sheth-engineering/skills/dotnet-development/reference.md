# .NET Development — reference

## Example

Request: add a scoped service that reads data via EF Core.

```csharp
// Program.cs (existing pattern: constructor-injected scoped services)
builder.Services.AddScoped<IOrderLookupService, OrderLookupService>();

// OrderLookupService.cs
public sealed class OrderLookupService : IOrderLookupService
{
    private readonly AppDbContext _db;

    public OrderLookupService(AppDbContext db) => _db = db;

    public async Task<OrderSummary?> GetSummaryAsync(
        int orderId, CancellationToken cancellationToken)
    {
        return await _db.Orders
            .AsNoTracking()
            .Where(o => o.Id == orderId)
            .Select(o => new OrderSummary(o.Id, o.Total, o.Status))
            .SingleOrDefaultAsync(cancellationToken);
    }
}
```

Note: registered as `Scoped` to match `AppDbContext`'s own scoped lifetime
(a singleton must never hold a scoped `DbContext` directly); uses
`AsNoTracking()` since this is a read-only lookup, matching
`CustomerLookupService` elsewhere in the project; `CancellationToken` is
threaded through per the project's existing convention.
