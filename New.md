Had to Run this to make the SQL access the tables 
// had to run in order to allow read access
// -- alter table public.people enable row level security;
// -- create policy "Public profiles are visible to everyone."
// -- on public.people for select
// -- to anon         -- the Postgres Role (recommended)
// -- using ( true ); -- the actual Policy

// -- alter table public.promotions enable row level security;
// -- create policy "Public profiles are visible to everyone."
// -- on public.promotions for select
// -- to anon         -- the Postgres Role (recommended)
// -- using ( true ); -- the actual Policy

// -- alter table public.transactions enable row level security;
// -- create policy "Public profiles are visible to everyone."
// -- on public.transactions for select
// -- to anon         -- the Postgres Role (recommended)
// -- using ( true ); -- the actual Policy

// alter table public.transfers enable row level security;
// create policy "Public profiles are visible to everyone."
// on public.transfers for select
// to anon         -- the Postgres Role (recommended)
// using ( true ); -- the actual Policy

//also ran this 
// -- Update client_email where it's missing but telephone has a match
// UPDATE public.promotions p
// SET client_email = pe.email
// FROM public.people pe
// WHERE (p.client_email IS NULL OR p.client_email = '') 
// AND p.telephone = pe.phone;

// -- Update telephone where it's missing but client_email has a match
// UPDATE public.promotions p
// SET telephone = pe.phone
// FROM public.people pe
// WHERE (p.telephone IS NULL OR p.telephone = '') 
// AND p.client_email = pe.email;
