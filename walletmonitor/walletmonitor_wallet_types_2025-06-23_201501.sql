--
-- PostgreSQL database dump
--

-- Dumped from database version 15.13 (Debian 15.13-1.pgdg120+1)
-- Dumped by pg_dump version 15.13 (Homebrew)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: wallet_types; Type: TABLE; Schema: public; Owner: walletmonitor
--

CREATE TABLE public.wallet_types (
    id bigint NOT NULL,
    name character varying(50) NOT NULL,
    description text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.wallet_types OWNER TO walletmonitor;

--
-- Name: TABLE wallet_types; Type: COMMENT; Schema: public; Owner: walletmonitor
--

COMMENT ON TABLE public.wallet_types IS 'Wallet type definitions';


--
-- Name: wallet_types_id_seq; Type: SEQUENCE; Schema: public; Owner: walletmonitor
--

CREATE SEQUENCE public.wallet_types_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.wallet_types_id_seq OWNER TO walletmonitor;

--
-- Name: wallet_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: walletmonitor
--

ALTER SEQUENCE public.wallet_types_id_seq OWNED BY public.wallet_types.id;


--
-- Name: wallet_types id; Type: DEFAULT; Schema: public; Owner: walletmonitor
--

ALTER TABLE ONLY public.wallet_types ALTER COLUMN id SET DEFAULT nextval('public.wallet_types_id_seq'::regclass);


--
-- Name: wallet_types wallet_types_name_key; Type: CONSTRAINT; Schema: public; Owner: walletmonitor
--

ALTER TABLE ONLY public.wallet_types
    ADD CONSTRAINT wallet_types_name_key UNIQUE (name);


--
-- Name: wallet_types wallet_types_pkey; Type: CONSTRAINT; Schema: public; Owner: walletmonitor
--

ALTER TABLE ONLY public.wallet_types
    ADD CONSTRAINT wallet_types_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

