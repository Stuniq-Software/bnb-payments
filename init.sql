CREATE TABLE IF NOT EXISTS bookings (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL REFERENCES users(id),
    stay_id uuid NOT NULL REFERENCES stays(id),
    checkin_date date NOT NULL,
    checkout_date date NOT NULL,
    nights integer NOT NULL,
    total_amount numeric(10, 2) NOT NULL,
    payment_id text,
    is_paid boolean DEFAULT false,
    status text NOT NULL DEFAULT 'confirmed',
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);

CREATE TABLE IF NOT EXISTS payments (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    booking_id uuid NOT NULL REFERENCES bookings(id),
    amount numeric(10, 2) NOT NULL,
    currency text NOT NULL,
    status text NOT NULL,
    payment_intent_id text NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);