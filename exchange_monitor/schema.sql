

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;


COMMENT ON SCHEMA "public" IS 'standard public schema';



CREATE EXTENSION IF NOT EXISTS "pg_graphql" WITH SCHEMA "graphql";






CREATE EXTENSION IF NOT EXISTS "pg_stat_statements" WITH SCHEMA "extensions";






CREATE EXTENSION IF NOT EXISTS "pgcrypto" WITH SCHEMA "extensions";






CREATE EXTENSION IF NOT EXISTS "supabase_vault" WITH SCHEMA "vault";






CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA "extensions";





SET default_tablespace = '';

SET default_table_access_method = "heap";


CREATE TABLE IF NOT EXISTS "public"."chains" (
    "id" bigint NOT NULL,
    "name" "text" NOT NULL,
    "native_sym" "text" NOT NULL
);


ALTER TABLE "public"."chains" OWNER TO "postgres";


CREATE SEQUENCE IF NOT EXISTS "public"."chains_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "public"."chains_id_seq" OWNER TO "postgres";


ALTER SEQUENCE "public"."chains_id_seq" OWNED BY "public"."chains"."id";



CREATE TABLE IF NOT EXISTS "public"."token_flows" (
    "id" integer NOT NULL,
    "token_id" integer NOT NULL,
    "chain_id" integer NOT NULL,
    "timestamp" integer NOT NULL,
    "inflow" numeric(20,6) NOT NULL,
    "outflow" numeric(20,6) NOT NULL,
    "inflow_count" integer NOT NULL,
    "outflow_count" integer NOT NULL,
    "net_flow" numeric(20,6) NOT NULL,
    "created_at" integer NOT NULL,
    "inflow_usd" numeric(20,6) DEFAULT 0 NOT NULL,
    "outflow_usd" numeric(20,6) DEFAULT 0 NOT NULL,
    "net_flow_usd" numeric(20,6) DEFAULT 0 NOT NULL
);


ALTER TABLE "public"."token_flows" OWNER TO "postgres";


CREATE SEQUENCE IF NOT EXISTS "public"."token_flows_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "public"."token_flows_id_seq" OWNER TO "postgres";


ALTER SEQUENCE "public"."token_flows_id_seq" OWNED BY "public"."token_flows"."id";



CREATE TABLE IF NOT EXISTS "public"."tokens" (
    "id" bigint NOT NULL,
    "symbol" "text" NOT NULL,
    "contract" "text",
    "chain_id" bigint NOT NULL,
    "decimals" smallint DEFAULT 18 NOT NULL
);


ALTER TABLE "public"."tokens" OWNER TO "postgres";


CREATE SEQUENCE IF NOT EXISTS "public"."tokens_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "public"."tokens_id_seq" OWNER TO "postgres";


ALTER SEQUENCE "public"."tokens_id_seq" OWNED BY "public"."tokens"."id";



CREATE TABLE IF NOT EXISTS "public"."transactions" (
    "id" bigint NOT NULL,
    "tx_hash" "text" NOT NULL,
    "chain_id" bigint NOT NULL,
    "block_height" bigint,
    "from_wallet_id" bigint NOT NULL,
    "to_wallet_id" bigint NOT NULL,
    "token_id" bigint NOT NULL,
    "amount" numeric(78,0) NOT NULL,
    "usd_value" numeric(38,10),
    "ts" timestamp with time zone NOT NULL,
    "raw_remark" "jsonb"
);


ALTER TABLE "public"."transactions" OWNER TO "postgres";


CREATE SEQUENCE IF NOT EXISTS "public"."transactions_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "public"."transactions_id_seq" OWNER TO "postgres";


ALTER SEQUENCE "public"."transactions_id_seq" OWNED BY "public"."transactions"."id";



CREATE TABLE IF NOT EXISTS "public"."wallet_balances" (
    "id" bigint NOT NULL,
    "wallet_id" bigint NOT NULL,
    "token_id" bigint NOT NULL,
    "chain_id" bigint NOT NULL,
    "amount" numeric(78,0) NOT NULL,
    "usd_value" numeric(38,10),
    "block_height" bigint,
    "ts" timestamp with time zone NOT NULL,
    "raw_remark" "jsonb",
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL
);


ALTER TABLE "public"."wallet_balances" OWNER TO "postgres";


CREATE SEQUENCE IF NOT EXISTS "public"."wallet_balances_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "public"."wallet_balances_id_seq" OWNER TO "postgres";


ALTER SEQUENCE "public"."wallet_balances_id_seq" OWNED BY "public"."wallet_balances"."id";



CREATE TABLE IF NOT EXISTS "public"."wallets" (
    "id" bigint NOT NULL,
    "address" "text" NOT NULL,
    "chain_id" bigint NOT NULL,
    "friendly_name" "text",
    "grp_type" "text",
    "grp_name" "text",
    "updated" boolean DEFAULT false
);


ALTER TABLE "public"."wallets" OWNER TO "postgres";


CREATE SEQUENCE IF NOT EXISTS "public"."wallets_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "public"."wallets_id_seq" OWNER TO "postgres";


ALTER SEQUENCE "public"."wallets_id_seq" OWNED BY "public"."wallets"."id";



ALTER TABLE ONLY "public"."chains" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."chains_id_seq"'::"regclass");



ALTER TABLE ONLY "public"."token_flows" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."token_flows_id_seq"'::"regclass");



ALTER TABLE ONLY "public"."tokens" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."tokens_id_seq"'::"regclass");



ALTER TABLE ONLY "public"."transactions" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."transactions_id_seq"'::"regclass");



ALTER TABLE ONLY "public"."wallet_balances" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."wallet_balances_id_seq"'::"regclass");



ALTER TABLE ONLY "public"."wallets" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."wallets_id_seq"'::"regclass");



ALTER TABLE ONLY "public"."chains"
    ADD CONSTRAINT "chains_name_key" UNIQUE ("name");



ALTER TABLE ONLY "public"."chains"
    ADD CONSTRAINT "chains_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."token_flows"
    ADD CONSTRAINT "token_flows_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."tokens"
    ADD CONSTRAINT "tokens_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."tokens"
    ADD CONSTRAINT "tokens_symbol_chain_id_key" UNIQUE ("symbol", "chain_id");



ALTER TABLE ONLY "public"."transactions"
    ADD CONSTRAINT "transactions_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."transactions"
    ADD CONSTRAINT "transactions_tx_hash_token_id_key" UNIQUE ("tx_hash", "token_id");



ALTER TABLE ONLY "public"."token_flows"
    ADD CONSTRAINT "unique_flow" UNIQUE ("token_id", "chain_id", "timestamp");



ALTER TABLE ONLY "public"."wallet_balances"
    ADD CONSTRAINT "wallet_balances_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."wallet_balances"
    ADD CONSTRAINT "wallet_balances_wallet_id_token_id_block_height_key" UNIQUE ("wallet_id", "token_id", "block_height");



ALTER TABLE ONLY "public"."wallets"
    ADD CONSTRAINT "wallets_address_chain_id_key" UNIQUE ("address", "chain_id");



ALTER TABLE ONLY "public"."wallets"
    ADD CONSTRAINT "wallets_pkey" PRIMARY KEY ("id");



CREATE INDEX "idx_token_flows_timestamp_token" ON "public"."token_flows" USING "btree" ("timestamp", "token_id");



CREATE INDEX "idx_token_symbol_chain" ON "public"."tokens" USING "btree" ("symbol", "chain_id");



CREATE INDEX "idx_tx_from_wallet" ON "public"."transactions" USING "btree" ("from_wallet_id", "ts" DESC);



CREATE INDEX "idx_tx_from_wallet_token" ON "public"."transactions" USING "btree" ("from_wallet_id", "token_id", "ts" DESC);



CREATE INDEX "idx_tx_to_wallet" ON "public"."transactions" USING "btree" ("to_wallet_id", "ts" DESC);



CREATE INDEX "idx_tx_to_wallet_token" ON "public"."transactions" USING "btree" ("to_wallet_id", "token_id", "ts" DESC);



CREATE INDEX "idx_wallet_address_chain" ON "public"."wallets" USING "btree" ("address", "chain_id");



CREATE INDEX "idx_wallet_balance_chain" ON "public"."wallet_balances" USING "btree" ("chain_id");



CREATE INDEX "idx_wallet_balance_ts" ON "public"."wallet_balances" USING "btree" ("ts" DESC);



CREATE INDEX "idx_wallet_balance_wallet_token" ON "public"."wallet_balances" USING "btree" ("wallet_id", "token_id", "ts" DESC);



CREATE UNIQUE INDEX "unique_tx_hash" ON "public"."transactions" USING "btree" ("tx_hash");



ALTER TABLE ONLY "public"."token_flows"
    ADD CONSTRAINT "token_flows_chain_id_fkey" FOREIGN KEY ("chain_id") REFERENCES "public"."chains"("id");



ALTER TABLE ONLY "public"."token_flows"
    ADD CONSTRAINT "token_flows_token_id_fkey" FOREIGN KEY ("token_id") REFERENCES "public"."tokens"("id");



ALTER TABLE ONLY "public"."wallet_balances"
    ADD CONSTRAINT "wallet_balances_chain_id_fkey" FOREIGN KEY ("chain_id") REFERENCES "public"."chains"("id");



ALTER TABLE ONLY "public"."wallet_balances"
    ADD CONSTRAINT "wallet_balances_token_id_fkey" FOREIGN KEY ("token_id") REFERENCES "public"."tokens"("id");



ALTER TABLE ONLY "public"."wallet_balances"
    ADD CONSTRAINT "wallet_balances_wallet_id_fkey" FOREIGN KEY ("wallet_id") REFERENCES "public"."wallets"("id");





ALTER PUBLICATION "supabase_realtime" OWNER TO "postgres";


GRANT USAGE ON SCHEMA "public" TO "postgres";
GRANT USAGE ON SCHEMA "public" TO "anon";
GRANT USAGE ON SCHEMA "public" TO "authenticated";
GRANT USAGE ON SCHEMA "public" TO "service_role";








































































































































































GRANT ALL ON TABLE "public"."chains" TO "anon";
GRANT ALL ON TABLE "public"."chains" TO "authenticated";
GRANT ALL ON TABLE "public"."chains" TO "service_role";



GRANT ALL ON SEQUENCE "public"."chains_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."chains_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."chains_id_seq" TO "service_role";



GRANT ALL ON TABLE "public"."token_flows" TO "anon";
GRANT ALL ON TABLE "public"."token_flows" TO "authenticated";
GRANT ALL ON TABLE "public"."token_flows" TO "service_role";



GRANT ALL ON SEQUENCE "public"."token_flows_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."token_flows_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."token_flows_id_seq" TO "service_role";



GRANT ALL ON TABLE "public"."tokens" TO "anon";
GRANT ALL ON TABLE "public"."tokens" TO "authenticated";
GRANT ALL ON TABLE "public"."tokens" TO "service_role";



GRANT ALL ON SEQUENCE "public"."tokens_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."tokens_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."tokens_id_seq" TO "service_role";



GRANT ALL ON TABLE "public"."transactions" TO "anon";
GRANT ALL ON TABLE "public"."transactions" TO "authenticated";
GRANT ALL ON TABLE "public"."transactions" TO "service_role";



GRANT ALL ON SEQUENCE "public"."transactions_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."transactions_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."transactions_id_seq" TO "service_role";



GRANT ALL ON TABLE "public"."wallet_balances" TO "anon";
GRANT ALL ON TABLE "public"."wallet_balances" TO "authenticated";
GRANT ALL ON TABLE "public"."wallet_balances" TO "service_role";



GRANT ALL ON SEQUENCE "public"."wallet_balances_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."wallet_balances_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."wallet_balances_id_seq" TO "service_role";



GRANT ALL ON TABLE "public"."wallets" TO "anon";
GRANT ALL ON TABLE "public"."wallets" TO "authenticated";
GRANT ALL ON TABLE "public"."wallets" TO "service_role";



GRANT ALL ON SEQUENCE "public"."wallets_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."wallets_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."wallets_id_seq" TO "service_role";









ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES  TO "postgres";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES  TO "anon";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES  TO "authenticated";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES  TO "service_role";






ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS  TO "postgres";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS  TO "anon";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS  TO "authenticated";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS  TO "service_role";






ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES  TO "postgres";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES  TO "anon";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES  TO "authenticated";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES  TO "service_role";






























RESET ALL;
