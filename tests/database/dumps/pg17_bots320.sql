--
-- PostgreSQL database dump
--

\restrict hWaft0QgrlLH46W8JijekVFUIVndqcAw4pgtBF8MQd9BRJC7Ur7E6skK8T9lh5c

-- Dumped from database version 17.11 (Debian 17.11-1.pgdg13+2)
-- Dumped by pg_dump version 17.11 (Debian 17.11-1.pgdg13+2)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- Name: auth_group; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone NOT NULL,
    is_superuser boolean NOT NULL,
    username character varying(30) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(75) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.auth_user_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.auth_user_groups_id_seq OWNED BY public.auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.auth_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.auth_user_id_seq OWNED BY public.auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.auth_user_user_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.auth_user_user_permissions_id_seq OWNED BY public.auth_user_user_permissions.id;


--
-- Name: ccode; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ccode (
    id integer NOT NULL,
    ccodeid_id character varying(35) NOT NULL,
    leftcode character varying(35) NOT NULL,
    rightcode character varying(70) NOT NULL,
    attr1 character varying(70) NOT NULL,
    attr2 character varying(35) NOT NULL,
    attr3 character varying(35) NOT NULL,
    attr4 character varying(35) NOT NULL,
    attr5 character varying(35) NOT NULL,
    attr6 character varying(35) NOT NULL,
    attr7 character varying(35) NOT NULL,
    attr8 character varying(35) NOT NULL
);


--
-- Name: ccode_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ccode_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ccode_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ccode_id_seq OWNED BY public.ccode.id;


--
-- Name: ccodetrigger; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ccodetrigger (
    ccodeid character varying(35) NOT NULL,
    ccodeid_desc text
);


--
-- Name: channel; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.channel (
    idchannel character varying(35) NOT NULL,
    inorout character varying(35) NOT NULL,
    type character varying(35) NOT NULL,
    charset character varying(35) NOT NULL,
    host character varying(256) NOT NULL,
    port integer,
    username character varying(35) NOT NULL,
    secret character varying(35) NOT NULL,
    starttls boolean NOT NULL,
    apop boolean NOT NULL,
    remove boolean NOT NULL,
    path character varying(256) NOT NULL,
    filename character varying(256) NOT NULL,
    lockname character varying(35) NOT NULL,
    syslock boolean NOT NULL,
    parameters character varying(70) NOT NULL,
    ftpaccount character varying(35) NOT NULL,
    ftpactive boolean NOT NULL,
    ftpbinary boolean NOT NULL,
    askmdn character varying(17) NOT NULL,
    sendmdn character varying(17) NOT NULL,
    mdnchannel character varying(35) NOT NULL,
    archivepath character varying(256) NOT NULL,
    "desc" text,
    rsrv1 character varying(35),
    rsrv2 integer,
    rsrv3 integer,
    keyfile character varying(256),
    certfile character varying(256),
    testpath character varying(256) NOT NULL,
    CONSTRAINT channel_port_check CHECK ((port >= 0))
);


--
-- Name: chanpar; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.chanpar (
    id integer NOT NULL,
    idpartner_id character varying(35) NOT NULL,
    idchannel_id character varying(35) NOT NULL,
    mail character varying(256) NOT NULL,
    cc character varying(256) NOT NULL,
    askmdn boolean NOT NULL,
    sendmdn boolean NOT NULL
);


--
-- Name: chanpar_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.chanpar_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: chanpar_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.chanpar_id_seq OWNED BY public.chanpar.id;


--
-- Name: confirmrule; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.confirmrule (
    id integer NOT NULL,
    active boolean NOT NULL,
    confirmtype character varying(35) NOT NULL,
    ruletype character varying(35) NOT NULL,
    negativerule boolean NOT NULL,
    frompartner_id character varying(35),
    topartner_id character varying(35),
    idroute character varying(35),
    idchannel_id character varying(35),
    editype character varying(35) NOT NULL,
    messagetype character varying(35) NOT NULL,
    rsrv1 character varying(35),
    rsrv2 integer
);


--
-- Name: confirmrule_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.confirmrule_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: confirmrule_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.confirmrule_id_seq OWNED BY public.confirmrule.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.django_migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


--
-- Name: filereport; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.filereport (
    idta integer NOT NULL,
    reportidta integer NOT NULL,
    statust integer NOT NULL,
    retransmit integer NOT NULL,
    idroute character varying(35) NOT NULL,
    fromchannel character varying(35) NOT NULL,
    tochannel character varying(35) NOT NULL,
    frompartner character varying(35) NOT NULL,
    topartner character varying(35) NOT NULL,
    frommail character varying(256) NOT NULL,
    tomail character varying(256) NOT NULL,
    ineditype character varying(35) NOT NULL,
    inmessagetype character varying(35) NOT NULL,
    outeditype character varying(35) NOT NULL,
    outmessagetype character varying(35) NOT NULL,
    incontenttype character varying(35) NOT NULL,
    outcontenttype character varying(35) NOT NULL,
    nrmessages integer NOT NULL,
    ts timestamp with time zone NOT NULL,
    infilename character varying(256) NOT NULL,
    inidta integer,
    outfilename character varying(256) NOT NULL,
    outidta integer NOT NULL,
    divtext character varying(35) NOT NULL,
    errortext text NOT NULL,
    rsrv1 character varying(35),
    rsrv2 integer,
    filesize integer
);


--
-- Name: mutex; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mutex (
    mutexk integer NOT NULL,
    mutexer integer DEFAULT 0,
    ts timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


--
-- Name: partner; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.partner (
    idpartner character varying(35) NOT NULL,
    active boolean NOT NULL,
    isgroup boolean NOT NULL,
    name character varying(256) NOT NULL,
    mail character varying(256) NOT NULL,
    cc character varying(256) NOT NULL,
    rsrv1 character varying(35),
    rsrv2 integer,
    name1 character varying(70),
    name2 character varying(70),
    name3 character varying(70),
    address1 character varying(70),
    address2 character varying(70),
    address3 character varying(70),
    city character varying(35),
    postalcode character varying(17),
    countrysubdivision character varying(9),
    countrycode character varying(3),
    phone1 character varying(17),
    phone2 character varying(17),
    startdate date,
    enddate date,
    "desc" text,
    attr1 character varying(35),
    attr2 character varying(35),
    attr3 character varying(35),
    attr4 character varying(35),
    attr5 character varying(35)
);


--
-- Name: partnergroup; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.partnergroup (
    id integer NOT NULL,
    from_partner_id character varying(35) NOT NULL,
    to_partner_id character varying(35) NOT NULL
);


--
-- Name: partnergroup_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.partnergroup_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: partnergroup_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.partnergroup_id_seq OWNED BY public.partnergroup.id;


--
-- Name: persist; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.persist (
    domein character varying(35) NOT NULL,
    botskey character varying(35) NOT NULL,
    content text,
    ts timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


--
-- Name: report; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.report (
    idta integer NOT NULL,
    lastreceived integer NOT NULL,
    lastdone integer NOT NULL,
    lastopen integer NOT NULL,
    lastok integer NOT NULL,
    lasterror integer NOT NULL,
    send integer NOT NULL,
    processerrors integer NOT NULL,
    ts timestamp with time zone NOT NULL,
    type character varying(35) NOT NULL,
    status boolean NOT NULL,
    rsrv1 character varying(35),
    rsrv2 integer,
    filesize integer,
    acceptance integer
);


--
-- Name: routes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.routes (
    id integer NOT NULL,
    idroute character varying(35) NOT NULL,
    seq integer NOT NULL,
    active boolean NOT NULL,
    fromchannel_id character varying(35),
    fromeditype character varying(35) NOT NULL,
    frommessagetype character varying(35) NOT NULL,
    tochannel_id character varying(35),
    toeditype character varying(35) NOT NULL,
    tomessagetype character varying(35) NOT NULL,
    alt character varying(35) NOT NULL,
    frompartner_id character varying(35),
    topartner_id character varying(35),
    frompartner_tochannel_id character varying(35),
    topartner_tochannel_id character varying(35),
    testindicator character varying(1) NOT NULL,
    translateind integer NOT NULL,
    notindefaultrun boolean NOT NULL,
    "desc" text,
    rsrv1 character varying(35),
    rsrv2 integer,
    defer boolean NOT NULL,
    zip_incoming integer,
    zip_outgoing integer,
    CONSTRAINT routes_seq_check CHECK ((seq >= 0))
);


--
-- Name: routes_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.routes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: routes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.routes_id_seq OWNED BY public.routes.id;


--
-- Name: ta; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ta (
    idta integer NOT NULL,
    statust integer DEFAULT 0,
    status integer DEFAULT 0,
    parent integer DEFAULT 0,
    child integer DEFAULT 0,
    script integer DEFAULT 0,
    idroute character varying(35) DEFAULT ''::character varying,
    filename character varying(256) DEFAULT ''::character varying,
    frompartner character varying(35) DEFAULT ''::character varying,
    topartner character varying(35) DEFAULT ''::character varying,
    fromchannel character varying(35) DEFAULT ''::character varying,
    tochannel character varying(35) DEFAULT ''::character varying,
    editype character varying(35) DEFAULT ''::character varying,
    messagetype character varying(35) DEFAULT ''::character varying,
    alt character varying(35) DEFAULT ''::character varying,
    divtext character varying(35) DEFAULT ''::character varying,
    merge boolean DEFAULT false,
    nrmessages integer DEFAULT 1,
    testindicator character varying(10) DEFAULT ''::character varying,
    reference character varying(70) DEFAULT ''::character varying,
    frommail character varying(256) DEFAULT ''::character varying,
    tomail character varying(256) DEFAULT ''::character varying,
    charset character varying(35) DEFAULT ''::character varying,
    statuse integer DEFAULT 0,
    retransmit boolean DEFAULT false,
    contenttype character varying(35) DEFAULT 'text/plain'::character varying,
    errortext text,
    ts timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    confirmasked boolean DEFAULT false,
    confirmed boolean DEFAULT false,
    confirmtype character varying(35) DEFAULT ''::character varying,
    confirmidta integer DEFAULT 0,
    envelope character varying(35) DEFAULT ''::character varying,
    botskey character varying(35) DEFAULT ''::character varying,
    cc character varying(512) DEFAULT ''::character varying,
    rsrv1 character varying(35) DEFAULT ''::character varying,
    rsrv2 integer DEFAULT 0,
    rsrv3 character varying(35) DEFAULT ''::character varying,
    rsrv4 integer DEFAULT 0,
    filesize integer DEFAULT 0,
    numberofresends integer DEFAULT 0,
    rsrv5 character varying(35) DEFAULT ''::character varying
);


--
-- Name: ta_idta_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ta_idta_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ta_idta_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ta_idta_seq OWNED BY public.ta.idta;


--
-- Name: translate; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.translate (
    id integer NOT NULL,
    active boolean NOT NULL,
    fromeditype character varying(35) NOT NULL,
    frommessagetype character varying(35) NOT NULL,
    alt character varying(35) NOT NULL,
    frompartner_id character varying(35),
    topartner_id character varying(35),
    tscript character varying(35) NOT NULL,
    toeditype character varying(35) NOT NULL,
    tomessagetype character varying(35) NOT NULL,
    "desc" text,
    rsrv1 character varying(35),
    rsrv2 integer
);


--
-- Name: translate_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.translate_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: translate_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.translate_id_seq OWNED BY public.translate.id;


--
-- Name: uniek; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.uniek (
    domein character varying(35) NOT NULL,
    nummer integer DEFAULT 1 NOT NULL
);


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: auth_user id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq'::regclass);


--
-- Name: auth_user_groups id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups ALTER COLUMN id SET DEFAULT nextval('public.auth_user_groups_id_seq'::regclass);


--
-- Name: auth_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_user_user_permissions_id_seq'::regclass);


--
-- Name: ccode id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ccode ALTER COLUMN id SET DEFAULT nextval('public.ccode_id_seq'::regclass);


--
-- Name: chanpar id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chanpar ALTER COLUMN id SET DEFAULT nextval('public.chanpar_id_seq'::regclass);


--
-- Name: confirmrule id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.confirmrule ALTER COLUMN id SET DEFAULT nextval('public.confirmrule_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Name: partnergroup id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.partnergroup ALTER COLUMN id SET DEFAULT nextval('public.partnergroup_id_seq'::regclass);


--
-- Name: routes id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.routes ALTER COLUMN id SET DEFAULT nextval('public.routes_id_seq'::regclass);


--
-- Name: ta idta; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ta ALTER COLUMN idta SET DEFAULT nextval('public.ta_idta_seq'::regclass);


--
-- Name: translate id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.translate ALTER COLUMN id SET DEFAULT nextval('public.translate_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_group (id, name) FROM stdin;
1	viewers
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
1	1	56
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add permission	1	add_permission
2	Can change permission	1	change_permission
3	Can delete permission	1	delete_permission
4	Can add group	2	add_group
5	Can change group	2	change_group
6	Can delete group	2	delete_group
7	Can add user	3	add_user
8	Can change user	3	change_user
9	Can delete user	3	delete_user
10	Can add content type	4	add_contenttype
11	Can change content type	4	change_contenttype
12	Can delete content type	4	delete_contenttype
13	Can add session	5	add_session
14	Can change session	5	change_session
15	Can delete session	5	delete_session
16	Can add log entry	6	add_logentry
17	Can change log entry	6	change_logentry
18	Can delete log entry	6	delete_logentry
19	Can add confirm rule	7	add_confirmrule
20	Can change confirm rule	7	change_confirmrule
21	Can delete confirm rule	7	delete_confirmrule
22	Can add user code type	8	add_ccodetrigger
23	Can change user code type	8	change_ccodetrigger
24	Can delete user code type	8	delete_ccodetrigger
25	Can add user code	9	add_ccode
26	Can change user code	9	change_ccode
27	Can delete user code	9	delete_ccode
28	Can add channel	10	add_channel
29	Can change channel	10	change_channel
30	Can delete channel	10	delete_channel
31	Can add partner	11	add_partner
32	Can change partner	11	change_partner
33	Can delete partner	11	delete_partner
34	Can add partnergroep	11	add_partnergroep
35	Can change partnergroep	11	change_partnergroep
36	Can delete partnergroep	11	delete_partnergroep
37	Can add email address per channel	12	add_chanpar
38	Can change email address per channel	12	change_chanpar
39	Can delete email address per channel	12	delete_chanpar
40	Can add translation rule	13	add_translate
41	Can change translation rule	13	change_translate
42	Can delete translation rule	13	delete_translate
43	Can add route	14	add_routes
44	Can change route	14	change_routes
45	Can delete route	14	delete_routes
46	Can add filereport	15	add_filereport
47	Can change filereport	15	change_filereport
48	Can delete filereport	15	delete_filereport
49	Can add mutex	16	add_mutex
50	Can change mutex	16	change_mutex
51	Can delete mutex	16	delete_mutex
52	Can add persist	17	add_persist
53	Can change persist	17	change_persist
54	Can delete persist	17	delete_persist
55	Can add report	18	add_report
56	Can change report	18	change_report
57	Can delete report	18	delete_report
58	Can add ta	19	add_ta
59	Can change ta	19	change_ta
60	Can delete ta	19	delete_ta
61	Can add counter	20	add_uniek
62	Can change counter	20	change_uniek
63	Can delete counter	20	delete_uniek
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
1	pbkdf2_sha256$15000$x5YcPXbLBahG$UKmr2bKDYzhdvqP7BdsXV/lTX6z990ALrMjojZJdijc=	2026-10-11 16:31:41.2059+00	t	bots			bots@example.org	t	t	2026-10-11 16:31:41.2059+00
2	pbkdf2_sha256$15000$f0yFDDy0MGp6$0ENar2FgBf/klN3MmPznkeFviHnG0CVUCWKxwC8u3HI=	2026-10-11 16:31:43.449022+00	f	operator			op@example.org	t	t	2026-10-11 16:31:43.449022+00
3	pbkdf2_sha256$15000$TEwV6Wmz66lC$xvMHXMeRFcFoy5RXMoRyL7TF7vhovMQ7Z4UKHT+elL4=	2026-10-11 16:31:47.602565+00	f	viewer			v@example.org	f	t	2026-10-11 16:31:47.602565+00
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
1	2	1
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
1	2	50
2	2	51
3	2	41
4	2	44
5	2	29
6	2	32
7	2	31
8	2	26
9	2	25
10	2	27
11	2	23
12	2	20
13	2	56
14	2	47
15	2	59
\.


--
-- Data for Name: ccode; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.ccode (id, ccodeid_id, leftcode, rightcode, attr1, attr2, attr3, attr4, attr5, attr6, attr7, attr8) FROM stdin;
1	x12_partner	FROMPARTNER2	frompartner1	WX							
2	x12_partner	TOPARTNER2	topartner1	YZ							
\.


--
-- Data for Name: ccodetrigger; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.ccodetrigger (ccodeid, ccodeid_desc) FROM stdin;
x12_partner	
\.


--
-- Data for Name: channel; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.channel (idchannel, inorout, type, charset, host, port, username, secret, starttls, apop, remove, path, filename, lockname, syslock, parameters, ftpaccount, ftpactive, ftpbinary, askmdn, sendmdn, mdnchannel, archivepath, "desc", rsrv1, rsrv2, rsrv3, keyfile, certfile, testpath) FROM stdin;
myfirstroute_in	in	file	us-ascii		0			f	f	f	botssys/infile/my_first_plugin	*.edi		f			f	f	no	no			\N	\N	\N	\N	\N	\N	
myfirstroute_out	out	file	us-ascii		0			f	f	f	botssys/outfile/my_first_plugin	orders*.inh		f			f	f	no	no			\N	\N	\N	\N	\N	\N	
inbound_orders_in	in	file	us-ascii		0			f	f	f	botssys/infile/edifact_xml/edifact	*.edi		f			f	f						\N	\N	\N			botssys/infile/edifact_xml/edifact
inbound_orders_out	out	file	us-ascii		0			f	f	f	botssys/outfile/edifact_xml/xml	orders_*.xml		f			f	f						\N	\N	\N			botssys/outfile/edifact_xml/xml
outbound_desadv_in	in	file	us-ascii		0			f	f	f	botssys/infile/edifact_xml/xml	desadv*.xml		f			f	t						\N	\N	\N			botssys/infile/edifact_xml/xml
outbound_desadv_out	out	file	us-ascii		0			f	f	f	botssys/outfile/edifact_xml/edifact	desadv*.edi		f			f	t						\N	\N	\N			botssys/outfile/edifact_xml/edifact
outbound_invoice_in	in	file	us-ascii		0			f	f	f	botssys/infile/edifact_xml/xml	invoic*.xml		f			f	t						\N	\N	\N			botssys/infile/edifact_xml/xml
outbound_invoice_out	out	file	unoa		0			f	f	f	botssys/outfile/edifact_xml/edifact	invoic*.edi		f			f	t						\N	\N	\N			botssys/outfile/edifact_xml/edifact
demo_partner_conversion_in	in	file	us-ascii		0			f	f	f	botssys/infile/demo_work_with_partners/partner_conversion	*		f			f	f						\N	\N	\N			
demo_partner_conversion_out	out	file	us-ascii		0			f	f	f	botssys/outfile/demo_work_with_partners/partner_conversion	{frompartner}_{topartner}_*.{editype}		f			f	f						\N	\N	\N			
outbound_asn_in	in	file	utf-8		0			f	f	f	botssys/infile/demo_work_with_partners/asn	*.xml		f			f	f						\N	\N	\N			
outbound_asn_out	out	file	us-ascii		0			f	f	f	botssys/outfile/demo_work_with_partners/outbound_856	{topartner}_{datetime:%Y%m%d}_*.x12		f			f	f						\N	\N	\N			
outbound_asn_out_partner2	out	file	us-ascii		0			f	f	f	botssys/outfile/demo_work_with_partners/outbound_856	{topartner}_{datetime:%Y%m%d}_*.x12		f			f	f						\N	\N	\N			
outbound_asn_out_pgroupA	out	file	us-ascii		0			f	f	f	botssys/outfile/demo_work_with_partners/outbound_856	{topartner}_pgroupA_{datetime:%Y%m%d}_*.x12		f			f	f						\N	\N	\N			
\.


--
-- Data for Name: chanpar; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.chanpar (id, idpartner_id, idchannel_id, mail, cc, askmdn, sendmdn) FROM stdin;
\.


--
-- Data for Name: confirmrule; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.confirmrule (id, active, confirmtype, ruletype, negativerule, frompartner_id, topartner_id, idroute, idchannel_id, editype, messagetype, rsrv1, rsrv2) FROM stdin;
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_content_type (id, name, app_label, model) FROM stdin;
1	permission	auth	permission
2	group	auth	group
3	user	auth	user
4	content type	contenttypes	contenttype
5	session	sessions	session
6	log entry	admin	logentry
7	confirm rule	bots	confirmrule
8	user code type	bots	ccodetrigger
9	user code	bots	ccode
10	channel	bots	channel
11	partner	bots	partner
12	email address per channel	bots	chanpar
13	translation rule	bots	translate
14	route	bots	routes
15	filereport	bots	filereport
16	mutex	bots	mutex
17	persist	bots	persist
18	report	bots	report
19	ta	bots	ta
20	counter	bots	uniek
21	partnergroep	bots	partnergroep
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2026-10-11 16:30:17.922184+00
2	auth	0001_initial	2026-10-11 16:30:20.712235+00
3	admin	0001_initial	2026-10-11 16:30:23.996737+00
4	sessions	0001_initial	2026-10-11 16:30:24.734139+00
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
\.


--
-- Data for Name: filereport; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.filereport (idta, reportidta, statust, retransmit, idroute, fromchannel, tochannel, frompartner, topartner, frommail, tomail, ineditype, inmessagetype, outeditype, outmessagetype, incontenttype, outcontenttype, nrmessages, ts, infilename, inidta, outfilename, outidta, divtext, errortext, rsrv1, rsrv2, filesize) FROM stdin;
8	3	3	0	demo_partner_conversion	demo_partner_conversion_in	demo_partner_conversion_out	(several values)	(several values)			x12	856004010	x12	856004010	text/plain	application/X12	1	2026-10-11 16:51:56.738141+00	/o/pg/bots/botssys/infile/demo_work_with_partners/partner_conversion/frompartner1_topartner1_1.x12	\N	/o/pg/bots/botssys/outfile/demo_work_with_partners/partner_conversion/frompartner1_topartner1_1.x12	20	inn2out			\N	1227
25	3	3	0	inbound_orders	inbound_orders_in	inbound_orders_out	PARTNER1	PARTNER2			edifact	ORDERSD96AUNEAN008	xml	orders	text/plain	text/xml 	3	2026-10-11 16:52:40.792503+00	/o/pg/bots/botssys/infile/edifact_xml/edifact/0T0000000004.edi	\N	(several values)	75	orders_edifact2xml			\N	775
27	3	3	0	inbound_orders	inbound_orders_in	inbound_orders_out	PARTNER1	PARTNER2			edifact	ORDERSD96AUNEAN008	xml	orders	text/plain	text/xml 	1	2026-10-11 16:52:43.992816+00	/o/pg/bots/botssys/infile/edifact_xml/edifact/0T0000000015.edi	\N	/o/pg/bots/botssys/outfile/edifact_xml/xml/orders_6.xml	76	orders_edifact2xml			\N	261
29	3	3	0	inbound_orders	inbound_orders_in	inbound_orders_out	PARTNER1	PARTNER2			edifact	ORDERSD96AUNEAN008	xml	orders	text/plain	text/xml 	1	2026-10-11 16:52:48.191659+00	/o/pg/bots/botssys/infile/edifact_xml/edifact/T0000000001.edi	\N	/o/pg/bots/botssys/outfile/edifact_xml/xml/orders_1.xml	71	orders_edifact2xml			\N	276
31	3	3	0	inbound_orders	inbound_orders_in	inbound_orders_out	PARTNER1	PARTNER2			edifact	ORDERSD96AUNEAN008	xml	orders	text/plain	text/xml 	1	2026-10-11 16:52:49.885223+00	/o/pg/bots/botssys/infile/edifact_xml/edifact/T0000000002.edi	\N	/o/pg/bots/botssys/outfile/edifact_xml/xml/orders_2.xml	72	orders_edifact2xml			\N	282
81	3	3	0	myfirstroute	myfirstroute_in	myfirstroute_out	8712345678906	PARTNER2			edifact	ORDERSD96AUNEAN008	xml	orders	text/plain	text/xml 	3	2026-10-11 16:54:16.873824+00	/o/pg/bots/botssys/infile/my_first_plugin/order01.edi	\N	(several values)	121	orders_edifact2xml			\N	916
83	3	3	0	myfirstroute	myfirstroute_in	myfirstroute_out	8712345678906	PARTNER2			edifact	ORDERSD96AUNEAN008	xml	orders	text/plain	text/xml 	1	2026-10-11 16:54:19.614246+00	/o/pg/bots/botssys/infile/my_first_plugin/order02.edi	\N	/o/pg/bots/botssys/outfile/my_first_plugin/orders4.inh	122	orders_edifact2xml			\N	269
85	3	3	0	myfirstroute	myfirstroute_in	myfirstroute_out	8712345678906	PARTNER2			edifact	ORDERSD96AUNEAN008	xml	orders	text/plain	text/xml 	1	2026-10-11 16:54:22.240475+00	/o/pg/bots/botssys/infile/my_first_plugin/order03.edi	\N	/o/pg/bots/botssys/outfile/my_first_plugin/orders5.inh	123	orders_edifact2xml			\N	265
128	3	3	0	outbound_asn	outbound_asn_in	outbound_asn_out	SENDER	PARTNER1			xml	asn	x12	856004010	text/plain	application/X12	1	2026-10-11 16:55:07.479252+00	/o/pg/bots/botssys/infile/demo_work_with_partners/asn/856_PARTNER1_03.xml	\N	/o/pg/bots/botssys/outfile/demo_work_with_partners/outbound_856/PARTNER1_20261011_1.x12	166	asn_xml2x12_default			\N	16468
130	3	3	0	outbound_asn	outbound_asn_in	outbound_asn_out_partner2	SENDER	PARTNER2			xml	asn	x12	856004010	text/plain	application/X12	1	2026-10-11 16:55:08.199825+00	/o/pg/bots/botssys/infile/demo_work_with_partners/asn/856_PARTNER2_01.xml	\N	/o/pg/bots/botssys/outfile/demo_work_with_partners/outbound_856/PARTNER2_20261011_1.x12	161	asn_xml2x12_partner2			\N	4523
132	3	3	0	outbound_asn	outbound_asn_in	outbound_asn_out_partner2	SENDER	PARTNER2			xml	asn	x12	856004010	text/plain	application/X12	1	2026-10-11 16:55:08.624136+00	/o/pg/bots/botssys/infile/demo_work_with_partners/asn/856_PARTNER2_04.xml	\N	/o/pg/bots/botssys/outfile/demo_work_with_partners/outbound_856/PARTNER2_20261011_1.x12	161	asn_xml2x12_partner2			\N	1192
134	3	3	0	outbound_asn	outbound_asn_in	outbound_asn_out_pgroupA	SENDER	PARTNER3			xml	asn	x12	856004010	text/plain	application/X12	1	2026-10-11 16:55:09.056136+00	/o/pg/bots/botssys/infile/demo_work_with_partners/asn/856_PARTNER3_02.xml	\N	/o/pg/bots/botssys/outfile/demo_work_with_partners/outbound_856/PARTNER3_pgroupA_20261011_1.x12	156	asn_xml2x12_noSSCC			\N	3396
171	3	3	0	outbound_desadv	outbound_desadv_in	outbound_desadv_out	5555555555555	1111111111111			xml	desadv	edifact	DESADVD96AUNEAN005	text/plain	application/EDIFACT	1	2026-10-11 16:56:01.016787+00	/o/pg/bots/botssys/infile/edifact_xml/xml/desadv1923.xml	\N	/o/pg/bots/botssys/outfile/edifact_xml/edifact/desadv1.edi	219	desadv_xml2edifact			\N	1320
173	3	3	0	outbound_desadv	outbound_desadv_in	outbound_desadv_out	5555555555555	1111111111111			xml	desadv	edifact	DESADVD96AUNEAN005	text/plain	application/EDIFACT	1	2026-10-11 16:56:06.477223+00	/o/pg/bots/botssys/infile/edifact_xml/xml/desadvfull01.xml	\N	/o/pg/bots/botssys/outfile/edifact_xml/edifact/desadv1.edi	219	desadv_xml2edifact			\N	11810
175	3	3	0	outbound_desadv	outbound_desadv_in	outbound_desadv_out	SENDER	RECEIVER			xml	desadv	edifact	DESADVD96AUNEAN005	text/plain	application/EDIFACT	1	2026-10-11 16:56:08.006982+00	/o/pg/bots/botssys/infile/edifact_xml/xml/desadvtest01.xml	\N	/o/pg/bots/botssys/outfile/edifact_xml/edifact/desadv5.edi	223	desadv_xml2edifact			\N	1571
177	3	3	0	outbound_desadv	outbound_desadv_in	outbound_desadv_out	5555555555555	1111111111111			xml	desadv	edifact	DESADVD96AUNEAN005	text/plain	application/EDIFACT	1	2026-10-11 16:56:09.425171+00	/o/pg/bots/botssys/infile/edifact_xml/xml/desadvtest5-1.xml	\N	/o/pg/bots/botssys/outfile/edifact_xml/edifact/desadv1.edi	219	desadv_xml2edifact			\N	1503
179	3	3	0	outbound_desadv	outbound_desadv_in	outbound_desadv_out	5555555555555	2222222222222			xml	desadv	edifact	DESADVD96AUNEAN005	text/plain	application/EDIFACT	1	2026-10-11 16:56:09.800825+00	/o/pg/bots/botssys/infile/edifact_xml/xml/desadvtest5-2.xml	\N	/o/pg/bots/botssys/outfile/edifact_xml/edifact/desadv2.edi	220	desadv_xml2edifact			\N	1503
181	3	3	0	outbound_desadv	outbound_desadv_in	outbound_desadv_out	6666666666666	1111111111111			xml	desadv	edifact	DESADVD96AUNEAN005	text/plain	application/EDIFACT	1	2026-10-11 16:56:10.522718+00	/o/pg/bots/botssys/infile/edifact_xml/xml/desadvtest6-1.xml	\N	/o/pg/bots/botssys/outfile/edifact_xml/edifact/desadv3.edi	221	desadv_xml2edifact			\N	1503
183	3	3	0	outbound_desadv	outbound_desadv_in	outbound_desadv_out	6666666666666	2222222222222			xml	desadv	edifact	DESADVD96AUNEAN005	text/plain	application/EDIFACT	1	2026-10-11 16:56:11.173876+00	/o/pg/bots/botssys/infile/edifact_xml/xml/desadvtest6-2.xml	\N	/o/pg/bots/botssys/outfile/edifact_xml/edifact/desadv4.edi	222	desadv_xml2edifact			\N	1503
228	3	3	0	outbound_invoice	outbound_invoice_in	outbound_invoice_out	5555555555555	1111111111111			xml	invoice	edifact	INVOICD96AUNEAN008	text/plain	application/EDIFACT	1	2026-10-11 16:56:44.92708+00	/o/pg/bots/botssys/infile/edifact_xml/xml/invoicfull01.xml	\N	/o/pg/bots/botssys/outfile/edifact_xml/edifact/invoic1.edi	271	invoice_xml2edifact			\N	5539
230	3	3	0	outbound_invoice	outbound_invoice_in	outbound_invoice_out	SENDER	RECEIVER			xml	invoice	edifact	INVOICD96AUNEAN008	text/plain	application/EDIFACT	1	2026-10-11 16:56:45.248535+00	/o/pg/bots/botssys/infile/edifact_xml/xml/invoictest01.xml	\N	/o/pg/bots/botssys/outfile/edifact_xml/edifact/invoic5.edi	275	invoice_xml2edifact			\N	2196
232	3	3	0	outbound_invoice	outbound_invoice_in	outbound_invoice_out	5555555555555	1111111111111			xml	invoice	edifact	INVOICD96AUNEAN008	text/plain	application/EDIFACT	1	2026-10-11 16:56:45.608677+00	/o/pg/bots/botssys/infile/edifact_xml/xml/invoictest5-1.xml	\N	/o/pg/bots/botssys/outfile/edifact_xml/edifact/invoic1.edi	271	invoice_xml2edifact			\N	2208
234	3	3	0	outbound_invoice	outbound_invoice_in	outbound_invoice_out	5555555555555	2222222222222			xml	invoice	edifact	INVOICD96AUNEAN008	text/plain	application/EDIFACT	1	2026-10-11 16:56:45.876759+00	/o/pg/bots/botssys/infile/edifact_xml/xml/invoictest5-2.xml	\N	/o/pg/bots/botssys/outfile/edifact_xml/edifact/invoic2.edi	272	invoice_xml2edifact			\N	2208
236	3	3	0	outbound_invoice	outbound_invoice_in	outbound_invoice_out	6666666666666	1111111111111			xml	invoice	edifact	INVOICD96AUNEAN008	text/plain	application/EDIFACT	1	2026-10-11 16:56:46.192444+00	/o/pg/bots/botssys/infile/edifact_xml/xml/invoictest6-1.xml	\N	/o/pg/bots/botssys/outfile/edifact_xml/edifact/invoic3.edi	273	invoice_xml2edifact			\N	2208
238	3	3	0	outbound_invoice	outbound_invoice_in	outbound_invoice_out	6666666666666	2222222222222			xml	invoice	edifact	INVOICD96AUNEAN008	text/plain	application/EDIFACT	1	2026-10-11 16:56:46.432567+00	/o/pg/bots/botssys/infile/edifact_xml/xml/invoictest6-2.xml	\N	/o/pg/bots/botssys/outfile/edifact_xml/edifact/invoic4.edi	274	invoice_xml2edifact			\N	2208
281	276	3	0	demo_partner_conversion	demo_partner_conversion_in	demo_partner_conversion_out	(several values)	(several values)			x12	856004010	x12	856004010	text/plain	application/X12	1	2026-10-11 16:57:57.642968+00	/o/pg/bots/botssys/infile/demo_work_with_partners/partner_conversion/frompartner1_topartner1_1.x12	\N	/o/pg/bots/botssys/outfile/demo_work_with_partners/partner_conversion/frompartner1_topartner1_2.x12	293	inn2out			\N	1227
298	276	3	0	inbound_orders	inbound_orders_in	inbound_orders_out	PARTNER1	PARTNER2			edifact	ORDERSD96AUNEAN008	xml	orders	text/plain	text/xml 	3	2026-10-11 16:58:12.475502+00	/o/pg/bots/botssys/infile/edifact_xml/edifact/0T0000000004.edi	\N	(several values)	346	orders_edifact2xml			\N	775
300	276	3	0	inbound_orders	inbound_orders_in	inbound_orders_out	PARTNER1	PARTNER2			edifact	ORDERSD96AUNEAN008	xml	orders	text/plain	text/xml 	1	2026-10-11 16:58:13.106957+00	/o/pg/bots/botssys/infile/edifact_xml/edifact/0T0000000015.edi	\N	/o/pg/bots/botssys/outfile/edifact_xml/xml/orders_10.xml	347	orders_edifact2xml			\N	261
302	276	3	0	inbound_orders	inbound_orders_in	inbound_orders_out	PARTNER1	PARTNER2			edifact	ORDERSD96AUNEAN008	xml	orders	text/plain	text/xml 	1	2026-10-11 16:58:13.575436+00	/o/pg/bots/botssys/infile/edifact_xml/edifact/T0000000001.edi	\N	/o/pg/bots/botssys/outfile/edifact_xml/xml/orders_11.xml	348	orders_edifact2xml			\N	276
304	276	3	0	inbound_orders	inbound_orders_in	inbound_orders_out	PARTNER1	PARTNER2			edifact	ORDERSD96AUNEAN008	xml	orders	text/plain	text/xml 	1	2026-10-11 16:58:14.143977+00	/o/pg/bots/botssys/infile/edifact_xml/edifact/T0000000002.edi	\N	/o/pg/bots/botssys/outfile/edifact_xml/xml/orders_12.xml	349	orders_edifact2xml			\N	282
354	276	3	0	myfirstroute	myfirstroute_in	myfirstroute_out	8712345678906	PARTNER2			edifact	ORDERSD96AUNEAN008	xml	orders	text/plain	text/xml 	3	2026-10-11 16:58:27.089776+00	/o/pg/bots/botssys/infile/my_first_plugin/order01.edi	\N	(several values)	394	orders_edifact2xml			\N	916
356	276	3	0	myfirstroute	myfirstroute_in	myfirstroute_out	8712345678906	PARTNER2			edifact	ORDERSD96AUNEAN008	xml	orders	text/plain	text/xml 	1	2026-10-11 16:58:27.77593+00	/o/pg/bots/botssys/infile/my_first_plugin/order02.edi	\N	/o/pg/bots/botssys/outfile/my_first_plugin/orders9.inh	395	orders_edifact2xml			\N	269
358	276	3	0	myfirstroute	myfirstroute_in	myfirstroute_out	8712345678906	PARTNER2			edifact	ORDERSD96AUNEAN008	xml	orders	text/plain	text/xml 	1	2026-10-11 16:58:28.237818+00	/o/pg/bots/botssys/infile/my_first_plugin/order03.edi	\N	/o/pg/bots/botssys/outfile/my_first_plugin/orders10.inh	396	orders_edifact2xml			\N	265
401	276	3	0	outbound_asn	outbound_asn_in	outbound_asn_out	SENDER	PARTNER1			xml	asn	x12	856004010	text/plain	application/X12	1	2026-10-11 16:58:40.750297+00	/o/pg/bots/botssys/infile/demo_work_with_partners/asn/856_PARTNER1_03.xml	\N	/o/pg/bots/botssys/outfile/demo_work_with_partners/outbound_856/PARTNER1_20261011_2.x12	439	asn_xml2x12_default			\N	16468
403	276	3	0	outbound_asn	outbound_asn_in	outbound_asn_out_partner2	SENDER	PARTNER2			xml	asn	x12	856004010	text/plain	application/X12	1	2026-10-11 16:58:41.053344+00	/o/pg/bots/botssys/infile/demo_work_with_partners/asn/856_PARTNER2_01.xml	\N	/o/pg/bots/botssys/outfile/demo_work_with_partners/outbound_856/PARTNER2_20261011_2.x12	434	asn_xml2x12_partner2			\N	4523
405	276	3	0	outbound_asn	outbound_asn_in	outbound_asn_out_partner2	SENDER	PARTNER2			xml	asn	x12	856004010	text/plain	application/X12	1	2026-10-11 16:58:41.439013+00	/o/pg/bots/botssys/infile/demo_work_with_partners/asn/856_PARTNER2_04.xml	\N	/o/pg/bots/botssys/outfile/demo_work_with_partners/outbound_856/PARTNER2_20261011_2.x12	434	asn_xml2x12_partner2			\N	1192
407	276	3	0	outbound_asn	outbound_asn_in	outbound_asn_out_pgroupA	SENDER	PARTNER3			xml	asn	x12	856004010	text/plain	application/X12	1	2026-10-11 16:58:41.773042+00	/o/pg/bots/botssys/infile/demo_work_with_partners/asn/856_PARTNER3_02.xml	\N	/o/pg/bots/botssys/outfile/demo_work_with_partners/outbound_856/PARTNER3_pgroupA_20261011_2.x12	429	asn_xml2x12_noSSCC			\N	3396
444	276	3	0	outbound_desadv	outbound_desadv_in	outbound_desadv_out	5555555555555	1111111111111			xml	desadv	edifact	DESADVD96AUNEAN005	text/plain	application/EDIFACT	1	2026-10-11 16:58:59.904938+00	/o/pg/bots/botssys/infile/edifact_xml/xml/desadv1923.xml	\N	/o/pg/bots/botssys/outfile/edifact_xml/edifact/desadv6.edi	492	desadv_xml2edifact			\N	1320
446	276	3	0	outbound_desadv	outbound_desadv_in	outbound_desadv_out	5555555555555	1111111111111			xml	desadv	edifact	DESADVD96AUNEAN005	text/plain	application/EDIFACT	1	2026-10-11 16:59:00.978926+00	/o/pg/bots/botssys/infile/edifact_xml/xml/desadvfull01.xml	\N	/o/pg/bots/botssys/outfile/edifact_xml/edifact/desadv6.edi	492	desadv_xml2edifact			\N	11810
448	276	3	0	outbound_desadv	outbound_desadv_in	outbound_desadv_out	SENDER	RECEIVER			xml	desadv	edifact	DESADVD96AUNEAN005	text/plain	application/EDIFACT	1	2026-10-11 16:59:02.054075+00	/o/pg/bots/botssys/infile/edifact_xml/xml/desadvtest01.xml	\N	/o/pg/bots/botssys/outfile/edifact_xml/edifact/desadv10.edi	496	desadv_xml2edifact			\N	1571
450	276	3	0	outbound_desadv	outbound_desadv_in	outbound_desadv_out	5555555555555	1111111111111			xml	desadv	edifact	DESADVD96AUNEAN005	text/plain	application/EDIFACT	1	2026-10-11 16:59:02.57327+00	/o/pg/bots/botssys/infile/edifact_xml/xml/desadvtest5-1.xml	\N	/o/pg/bots/botssys/outfile/edifact_xml/edifact/desadv6.edi	492	desadv_xml2edifact			\N	1503
452	276	3	0	outbound_desadv	outbound_desadv_in	outbound_desadv_out	5555555555555	2222222222222			xml	desadv	edifact	DESADVD96AUNEAN005	text/plain	application/EDIFACT	1	2026-10-11 16:59:03.409397+00	/o/pg/bots/botssys/infile/edifact_xml/xml/desadvtest5-2.xml	\N	/o/pg/bots/botssys/outfile/edifact_xml/edifact/desadv7.edi	493	desadv_xml2edifact			\N	1503
454	276	3	0	outbound_desadv	outbound_desadv_in	outbound_desadv_out	6666666666666	1111111111111			xml	desadv	edifact	DESADVD96AUNEAN005	text/plain	application/EDIFACT	1	2026-10-11 16:59:04.004468+00	/o/pg/bots/botssys/infile/edifact_xml/xml/desadvtest6-1.xml	\N	/o/pg/bots/botssys/outfile/edifact_xml/edifact/desadv8.edi	494	desadv_xml2edifact			\N	1503
456	276	3	0	outbound_desadv	outbound_desadv_in	outbound_desadv_out	6666666666666	2222222222222			xml	desadv	edifact	DESADVD96AUNEAN005	text/plain	application/EDIFACT	1	2026-10-11 16:59:04.466915+00	/o/pg/bots/botssys/infile/edifact_xml/xml/desadvtest6-2.xml	\N	/o/pg/bots/botssys/outfile/edifact_xml/edifact/desadv9.edi	495	desadv_xml2edifact			\N	1503
501	276	3	0	outbound_invoice	outbound_invoice_in	outbound_invoice_out	5555555555555	1111111111111			xml	invoice	edifact	INVOICD96AUNEAN008	text/plain	application/EDIFACT	1	2026-10-11 16:59:29.28574+00	/o/pg/bots/botssys/infile/edifact_xml/xml/invoicfull01.xml	\N	/o/pg/bots/botssys/outfile/edifact_xml/edifact/invoic6.edi	544	invoice_xml2edifact			\N	5539
503	276	3	0	outbound_invoice	outbound_invoice_in	outbound_invoice_out	SENDER	RECEIVER			xml	invoice	edifact	INVOICD96AUNEAN008	text/plain	application/EDIFACT	1	2026-10-11 16:59:29.562855+00	/o/pg/bots/botssys/infile/edifact_xml/xml/invoictest01.xml	\N	/o/pg/bots/botssys/outfile/edifact_xml/edifact/invoic10.edi	548	invoice_xml2edifact			\N	2196
505	276	3	0	outbound_invoice	outbound_invoice_in	outbound_invoice_out	5555555555555	1111111111111			xml	invoice	edifact	INVOICD96AUNEAN008	text/plain	application/EDIFACT	1	2026-10-11 16:59:30.014981+00	/o/pg/bots/botssys/infile/edifact_xml/xml/invoictest5-1.xml	\N	/o/pg/bots/botssys/outfile/edifact_xml/edifact/invoic6.edi	544	invoice_xml2edifact			\N	2208
507	276	3	0	outbound_invoice	outbound_invoice_in	outbound_invoice_out	5555555555555	2222222222222			xml	invoice	edifact	INVOICD96AUNEAN008	text/plain	application/EDIFACT	1	2026-10-11 16:59:30.738649+00	/o/pg/bots/botssys/infile/edifact_xml/xml/invoictest5-2.xml	\N	/o/pg/bots/botssys/outfile/edifact_xml/edifact/invoic7.edi	545	invoice_xml2edifact			\N	2208
509	276	3	0	outbound_invoice	outbound_invoice_in	outbound_invoice_out	6666666666666	1111111111111			xml	invoice	edifact	INVOICD96AUNEAN008	text/plain	application/EDIFACT	1	2026-10-11 16:59:31.194702+00	/o/pg/bots/botssys/infile/edifact_xml/xml/invoictest6-1.xml	\N	/o/pg/bots/botssys/outfile/edifact_xml/edifact/invoic8.edi	546	invoice_xml2edifact			\N	2208
511	276	3	0	outbound_invoice	outbound_invoice_in	outbound_invoice_out	6666666666666	2222222222222			xml	invoice	edifact	INVOICD96AUNEAN008	text/plain	application/EDIFACT	1	2026-10-11 16:59:31.686129+00	/o/pg/bots/botssys/infile/edifact_xml/xml/invoictest6-2.xml	\N	/o/pg/bots/botssys/outfile/edifact_xml/edifact/invoic9.edi	547	invoice_xml2edifact			\N	2208
554	549	3	0	demo_partner_conversion	demo_partner_conversion_in	demo_partner_conversion_out	(several values)	(several values)			x12	856004010	x12	856004010	text/plain	application/X12	1	2026-10-12 03:50:49.103872+00	/o/pg/bots/botssys/infile/demo_work_with_partners/partner_conversion/frompartner1_topartner1_1.x12	\N	/o/pg/bots/botssys/outfile/demo_work_with_partners/partner_conversion/frompartner1_topartner1_3.x12	566	inn2out			\N	1227
571	549	3	0	inbound_orders	inbound_orders_in	inbound_orders_out	PARTNER1	PARTNER2			edifact	ORDERSD96AUNEAN008	xml	orders	text/plain	text/xml 	3	2026-10-12 03:50:50.686642+00	/o/pg/bots/botssys/infile/edifact_xml/edifact/0T0000000004.edi	\N	(several values)	619	orders_edifact2xml			\N	775
573	549	3	0	inbound_orders	inbound_orders_in	inbound_orders_out	PARTNER1	PARTNER2			edifact	ORDERSD96AUNEAN008	xml	orders	text/plain	text/xml 	1	2026-10-12 03:50:50.725902+00	/o/pg/bots/botssys/infile/edifact_xml/edifact/0T0000000015.edi	\N	/o/pg/bots/botssys/outfile/edifact_xml/xml/orders_16.xml	620	orders_edifact2xml			\N	261
575	549	3	0	inbound_orders	inbound_orders_in	inbound_orders_out	PARTNER1	PARTNER2			edifact	ORDERSD96AUNEAN008	xml	orders	text/plain	text/xml 	1	2026-10-12 03:50:50.759433+00	/o/pg/bots/botssys/infile/edifact_xml/edifact/T0000000001.edi	\N	/o/pg/bots/botssys/outfile/edifact_xml/xml/orders_17.xml	621	orders_edifact2xml			\N	276
577	549	3	0	inbound_orders	inbound_orders_in	inbound_orders_out	PARTNER1	PARTNER2			edifact	ORDERSD96AUNEAN008	xml	orders	text/plain	text/xml 	1	2026-10-12 03:50:50.78515+00	/o/pg/bots/botssys/infile/edifact_xml/edifact/T0000000002.edi	\N	/o/pg/bots/botssys/outfile/edifact_xml/xml/orders_18.xml	622	orders_edifact2xml			\N	282
627	549	3	0	myfirstroute	myfirstroute_in	myfirstroute_out	8712345678906	PARTNER2			edifact	ORDERSD96AUNEAN008	xml	orders	text/plain	text/xml 	3	2026-10-12 03:50:51.934208+00	/o/pg/bots/botssys/infile/my_first_plugin/order01.edi	\N	(several values)	667	orders_edifact2xml			\N	916
629	549	3	0	myfirstroute	myfirstroute_in	myfirstroute_out	8712345678906	PARTNER2			edifact	ORDERSD96AUNEAN008	xml	orders	text/plain	text/xml 	1	2026-10-12 03:50:51.957258+00	/o/pg/bots/botssys/infile/my_first_plugin/order02.edi	\N	/o/pg/bots/botssys/outfile/my_first_plugin/orders14.inh	668	orders_edifact2xml			\N	269
631	549	3	0	myfirstroute	myfirstroute_in	myfirstroute_out	8712345678906	PARTNER2			edifact	ORDERSD96AUNEAN008	xml	orders	text/plain	text/xml 	1	2026-10-12 03:50:51.982854+00	/o/pg/bots/botssys/infile/my_first_plugin/order03.edi	\N	/o/pg/bots/botssys/outfile/my_first_plugin/orders15.inh	669	orders_edifact2xml			\N	265
674	549	3	0	outbound_asn	outbound_asn_in	outbound_asn_out	SENDER	PARTNER1			xml	asn	x12	856004010	text/plain	application/X12	1	2026-10-12 03:50:52.987153+00	/o/pg/bots/botssys/infile/demo_work_with_partners/asn/856_PARTNER1_03.xml	\N	/o/pg/bots/botssys/outfile/demo_work_with_partners/outbound_856/PARTNER1_20261012_3.x12	712	asn_xml2x12_default			\N	16468
676	549	3	0	outbound_asn	outbound_asn_in	outbound_asn_out_partner2	SENDER	PARTNER2			xml	asn	x12	856004010	text/plain	application/X12	1	2026-10-12 03:50:53.022666+00	/o/pg/bots/botssys/infile/demo_work_with_partners/asn/856_PARTNER2_01.xml	\N	/o/pg/bots/botssys/outfile/demo_work_with_partners/outbound_856/PARTNER2_20261012_3.x12	707	asn_xml2x12_partner2			\N	4523
678	549	3	0	outbound_asn	outbound_asn_in	outbound_asn_out_partner2	SENDER	PARTNER2			xml	asn	x12	856004010	text/plain	application/X12	1	2026-10-12 03:50:53.044303+00	/o/pg/bots/botssys/infile/demo_work_with_partners/asn/856_PARTNER2_04.xml	\N	/o/pg/bots/botssys/outfile/demo_work_with_partners/outbound_856/PARTNER2_20261012_3.x12	707	asn_xml2x12_partner2			\N	1192
680	549	3	0	outbound_asn	outbound_asn_in	outbound_asn_out_pgroupA	SENDER	PARTNER3			xml	asn	x12	856004010	text/plain	application/X12	1	2026-10-12 03:50:53.066839+00	/o/pg/bots/botssys/infile/demo_work_with_partners/asn/856_PARTNER3_02.xml	\N	/o/pg/bots/botssys/outfile/demo_work_with_partners/outbound_856/PARTNER3_pgroupA_20261012_3.x12	702	asn_xml2x12_noSSCC			\N	3396
717	549	3	0	outbound_desadv	outbound_desadv_in	outbound_desadv_out	5555555555555	1111111111111			xml	desadv	edifact	DESADVD96AUNEAN005	text/plain	application/EDIFACT	1	2026-10-12 03:50:53.940487+00	/o/pg/bots/botssys/infile/edifact_xml/xml/desadv1923.xml	\N	/o/pg/bots/botssys/outfile/edifact_xml/edifact/desadv11.edi	765	desadv_xml2edifact			\N	1320
719	549	3	0	outbound_desadv	outbound_desadv_in	outbound_desadv_out	5555555555555	1111111111111			xml	desadv	edifact	DESADVD96AUNEAN005	text/plain	application/EDIFACT	1	2026-10-12 03:50:53.972786+00	/o/pg/bots/botssys/infile/edifact_xml/xml/desadvfull01.xml	\N	/o/pg/bots/botssys/outfile/edifact_xml/edifact/desadv11.edi	765	desadv_xml2edifact			\N	11810
721	549	3	0	outbound_desadv	outbound_desadv_in	outbound_desadv_out	SENDER	RECEIVER			xml	desadv	edifact	DESADVD96AUNEAN005	text/plain	application/EDIFACT	1	2026-10-12 03:50:53.998711+00	/o/pg/bots/botssys/infile/edifact_xml/xml/desadvtest01.xml	\N	/o/pg/bots/botssys/outfile/edifact_xml/edifact/desadv15.edi	769	desadv_xml2edifact			\N	1571
723	549	3	0	outbound_desadv	outbound_desadv_in	outbound_desadv_out	5555555555555	1111111111111			xml	desadv	edifact	DESADVD96AUNEAN005	text/plain	application/EDIFACT	1	2026-10-12 03:50:54.024325+00	/o/pg/bots/botssys/infile/edifact_xml/xml/desadvtest5-1.xml	\N	/o/pg/bots/botssys/outfile/edifact_xml/edifact/desadv11.edi	765	desadv_xml2edifact			\N	1503
725	549	3	0	outbound_desadv	outbound_desadv_in	outbound_desadv_out	5555555555555	2222222222222			xml	desadv	edifact	DESADVD96AUNEAN005	text/plain	application/EDIFACT	1	2026-10-12 03:50:54.049553+00	/o/pg/bots/botssys/infile/edifact_xml/xml/desadvtest5-2.xml	\N	/o/pg/bots/botssys/outfile/edifact_xml/edifact/desadv12.edi	766	desadv_xml2edifact			\N	1503
727	549	3	0	outbound_desadv	outbound_desadv_in	outbound_desadv_out	6666666666666	1111111111111			xml	desadv	edifact	DESADVD96AUNEAN005	text/plain	application/EDIFACT	1	2026-10-12 03:50:54.089202+00	/o/pg/bots/botssys/infile/edifact_xml/xml/desadvtest6-1.xml	\N	/o/pg/bots/botssys/outfile/edifact_xml/edifact/desadv13.edi	767	desadv_xml2edifact			\N	1503
729	549	3	0	outbound_desadv	outbound_desadv_in	outbound_desadv_out	6666666666666	2222222222222			xml	desadv	edifact	DESADVD96AUNEAN005	text/plain	application/EDIFACT	1	2026-10-12 03:50:54.121764+00	/o/pg/bots/botssys/infile/edifact_xml/xml/desadvtest6-2.xml	\N	/o/pg/bots/botssys/outfile/edifact_xml/edifact/desadv14.edi	768	desadv_xml2edifact			\N	1503
774	549	3	0	outbound_invoice	outbound_invoice_in	outbound_invoice_out	5555555555555	1111111111111			xml	invoice	edifact	INVOICD96AUNEAN008	text/plain	application/EDIFACT	1	2026-10-12 03:50:55.328772+00	/o/pg/bots/botssys/infile/edifact_xml/xml/invoicfull01.xml	\N	/o/pg/bots/botssys/outfile/edifact_xml/edifact/invoic11.edi	817	invoice_xml2edifact			\N	5539
776	549	3	0	outbound_invoice	outbound_invoice_in	outbound_invoice_out	SENDER	RECEIVER			xml	invoice	edifact	INVOICD96AUNEAN008	text/plain	application/EDIFACT	1	2026-10-12 03:50:55.3624+00	/o/pg/bots/botssys/infile/edifact_xml/xml/invoictest01.xml	\N	/o/pg/bots/botssys/outfile/edifact_xml/edifact/invoic15.edi	821	invoice_xml2edifact			\N	2196
778	549	3	0	outbound_invoice	outbound_invoice_in	outbound_invoice_out	5555555555555	1111111111111			xml	invoice	edifact	INVOICD96AUNEAN008	text/plain	application/EDIFACT	1	2026-10-12 03:50:55.391896+00	/o/pg/bots/botssys/infile/edifact_xml/xml/invoictest5-1.xml	\N	/o/pg/bots/botssys/outfile/edifact_xml/edifact/invoic11.edi	817	invoice_xml2edifact			\N	2208
780	549	3	0	outbound_invoice	outbound_invoice_in	outbound_invoice_out	5555555555555	2222222222222			xml	invoice	edifact	INVOICD96AUNEAN008	text/plain	application/EDIFACT	1	2026-10-12 03:50:55.417601+00	/o/pg/bots/botssys/infile/edifact_xml/xml/invoictest5-2.xml	\N	/o/pg/bots/botssys/outfile/edifact_xml/edifact/invoic12.edi	818	invoice_xml2edifact			\N	2208
782	549	3	0	outbound_invoice	outbound_invoice_in	outbound_invoice_out	6666666666666	1111111111111			xml	invoice	edifact	INVOICD96AUNEAN008	text/plain	application/EDIFACT	1	2026-10-12 03:50:55.446852+00	/o/pg/bots/botssys/infile/edifact_xml/xml/invoictest6-1.xml	\N	/o/pg/bots/botssys/outfile/edifact_xml/edifact/invoic13.edi	819	invoice_xml2edifact			\N	2208
784	549	3	0	outbound_invoice	outbound_invoice_in	outbound_invoice_out	6666666666666	2222222222222			xml	invoice	edifact	INVOICD96AUNEAN008	text/plain	application/EDIFACT	1	2026-10-12 03:50:55.478951+00	/o/pg/bots/botssys/infile/edifact_xml/xml/invoictest6-2.xml	\N	/o/pg/bots/botssys/outfile/edifact_xml/edifact/invoic14.edi	820	invoice_xml2edifact			\N	2208
\.


--
-- Data for Name: mutex; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.mutex (mutexk, mutexer, ts) FROM stdin;
\.


--
-- Data for Name: partner; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.partner (idpartner, active, isgroup, name, mail, cc, rsrv1, rsrv2, name1, name2, name3, address1, address2, address3, city, postalcode, countrysubdivision, countrycode, phone1, phone2, startdate, enddate, "desc", attr1, attr2, attr3, attr4, attr5) FROM stdin;
PGROUP_A	t	t	Partnergroup A			\N	\N													\N	\N	\N					
PGROUP_B	t	t	Partnergroup B			\N	\N													\N	\N	\N					
PARTNER1	t	f	Partner 1			\N	\N													\N	\N	\N	XXXXXXXXXXXXXXXX				
PARTNER2	t	f	Partner 2			\N	\N													\N	\N	\N	PARTNER2LOOKUP				
PARTNER3	t	f	Partner 3			\N	\N													\N	\N	\N	8712345678906				
\.


--
-- Data for Name: partnergroup; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.partnergroup (id, from_partner_id, to_partner_id) FROM stdin;
1	PARTNER3	PGROUP_A
2	PARTNER3	PGROUP_B
\.


--
-- Data for Name: persist; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.persist (domein, botskey, content, ts) FROM stdin;
audit_domain	key1	(dp1\nS'a'\nI1\nsS'raw'\np2\nS'abc\\xff\\x00'\np3\nsS'txt'\np4\nVcafé \\u20ac\np5\ns.	2026-10-11 16:32:11.852794
audit_domain	kéy2	(lp1\nI1\naF2.5\naNaV\\u4e2d\na.	2026-10-11 16:32:12.001065
\.


--
-- Data for Name: report; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.report (idta, lastreceived, lastdone, lastopen, lastok, lasterror, send, processerrors, ts, type, status, rsrv1, rsrv2, filesize, acceptance) FROM stdin;
1	0	0	0	0	0	0	0	2026-10-11 16:32:08.504959+00	new	f		\N	0	0
2	0	0	0	0	0	0	0	2026-10-11 16:32:15.227237+00	new	f		\N	0	0
3	25	25	0	0	0	25	0	2026-10-11 16:51:49.853206+00	new	f		\N	67130	0
276	25	25	0	0	0	25	0	2026-10-11 16:57:56.291759+00	new	f		\N	67130	0
549	25	25	0	0	0	25	0	2026-10-12 03:50:48.820958+00	new	f		\N	67130	0
\.


--
-- Data for Name: routes; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.routes (id, idroute, seq, active, fromchannel_id, fromeditype, frommessagetype, tochannel_id, toeditype, tomessagetype, alt, frompartner_id, topartner_id, frompartner_tochannel_id, topartner_tochannel_id, testindicator, translateind, notindefaultrun, "desc", rsrv1, rsrv2, defer, zip_incoming, zip_outgoing) FROM stdin;
1	myfirstroute	9999	t	myfirstroute_in	edifact	edifact	myfirstroute_out				\N	\N	\N	\N		1	f	\N	\N	\N	f	\N	\N
2	inbound_orders	1	t	inbound_orders_in	edifact	edifact	inbound_orders_out				\N	\N	\N	\N		1	f		\N	\N	f	\N	\N
3	outbound_desadv	1	t	outbound_desadv_in	xml	desadv	outbound_desadv_out				\N	\N	\N	\N		1	f		\N	\N	f	\N	\N
4	outbound_invoice	1	t	outbound_invoice_in	xml	invoice	outbound_invoice_out				\N	\N	\N	\N		1	f		\N	\N	f	\N	\N
5	demo_partner_conversion	1	t	demo_partner_conversion_in	x12	x12	demo_partner_conversion_out				\N	\N	\N	\N		1	f	simple route: reads x12 856, and write these.\r\nthis route demo's conversion of partnerID's for x12:\r\n- incoming via QUERIES\r\n- outgoing via envelope script. 	\N	\N	f	\N	\N
6	outbound_asn	1	t	outbound_asn_in	xml	asn	\N				\N	\N	\N	\N		1	f		\N	\N	f	\N	\N
7	outbound_asn	101	t	\N			outbound_asn_out_pgroupA				\N	\N	\N	PGROUP_A		0	f		\N	\N	f	\N	\N
8	outbound_asn	102	t	\N			outbound_asn_out_partner2				\N	\N	\N	PARTNER2		0	f		\N	\N	f	\N	\N
9	outbound_asn	103	t	\N			outbound_asn_out				\N	\N	\N	\N		0	f		\N	\N	f	\N	\N
\.


--
-- Data for Name: ta; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.ta (idta, statust, status, parent, child, script, idroute, filename, frompartner, topartner, fromchannel, tochannel, editype, messagetype, alt, divtext, merge, nrmessages, testindicator, reference, frommail, tomail, charset, statuse, retransmit, contenttype, errortext, ts, confirmasked, confirmed, confirmtype, confirmidta, envelope, botskey, cc, rsrv1, rsrv2, rsrv3, rsrv4, filesize, numberofresends, rsrv5) FROM stdin;
8	3	200	0	0	7	demo_partner_conversion	/o/pg/bots/botssys/infile/demo_work_with_partners/partner_conversion/frompartner1_topartner1_1.x12			demo_partner_conversion_in						f	1						0	f	text/plain	\N	2026-10-11 16:51:56.738141	f	f		0					0		0	0	0	
7	3	1	0	0	6	demo_partner_conversion	incommunicate									f	1						0	f	text/plain	\N	2026-10-11 16:51:56.355221	f	f		0					0		0	0	0	
6	3	1	0	0	5	demo_partner_conversion	run			demo_partner_conversion_in						f	1						0	f	text/plain	\N	2026-10-11 16:51:51.386551	f	f		0					0		0	0	0	
16	3	400	0	0	5	demo_partner_conversion	16	frompartner1	topartner1	demo_partner_conversion_in		x12	856004010			t	1	P	1			us-ascii	0	f	application/X12	\N	2026-10-11 16:52:22.841479	f	f		0	x12				0		0	1227	0	
9	3	220	8	0	7	demo_partner_conversion	9			demo_partner_conversion_in		x12	x12			f	1						0	f	text/plain	\N	2026-10-11 16:51:57.475733	f	f		0					0		0	1229	0	
10	3	1	0	0	5	demo_partner_conversion	preprocess									f	1						0	f	text/plain	\N	2026-10-11 16:51:58.7311	f	f		0					0		0	0	0	
549	3	1	0	0	0		rundispatcher									f	1						0	f	text/plain	\N	2026-10-12 03:50:48.820958	f	f		0					0		0	0	0	
14	3	320	13	0	12	demo_partner_conversion	11	FROMPARTNER2	TOPARTNER2	demo_partner_conversion_in		x12	856004010		inn2out	t	1	P	0004			us-ascii	0	f	application/X12	\N	2026-10-11 16:52:19.742614	f	f		0	x12				0		0	0	0	
13	3	310	11	0	12	demo_partner_conversion	11	FROMPARTNER2	TOPARTNER2	demo_partner_conversion_in		x12	x12			t	1	P				us-ascii	0	f	application/X12	\N	2026-10-11 16:52:01.521077	f	f		0	x12				0		0	1227	0	
11	3	220	9	0	10	demo_partner_conversion	11			demo_partner_conversion_in		x12	x12			f	1						0	f	text/plain	\N	2026-10-11 16:51:59.12149	f	f		0					0		0	1227	0	
12	3	1	0	0	5	demo_partner_conversion	translate									f	1						0	f	text/plain	\N	2026-10-11 16:52:01.31298	f	f		0					0		0	0	0	
15	3	330	14	16	12	demo_partner_conversion	15	FROMPARTNER2	TOPARTNER2	demo_partner_conversion_in		x12	856004010		inn2out	t	1	P	1			us-ascii	0	f	application/X12	\N	2026-10-11 16:52:20.181605	f	f		0	x12				0		0	1037	0	
25	3	200	0	0	24	inbound_orders	/o/pg/bots/botssys/infile/edifact_xml/edifact/0T0000000004.edi			inbound_orders_in						f	1						0	f	text/plain	\N	2026-10-11 16:52:40.792503	f	f		0					0		0	0	0	
20	3	520	17	0	19	demo_partner_conversion	/o/pg/bots/botssys/outfile/demo_work_with_partners/partner_conversion/frompartner1_topartner1_1.x12	frompartner1	topartner1	demo_partner_conversion_in	demo_partner_conversion_out	x12	856004010			t	1	P	1			us-ascii	0	f	application/X12	\N	2026-10-11 16:52:28.7905	f	f		0	x12				0		0	0	1	
17	3	500	16	0	5	demo_partner_conversion	16	frompartner1	topartner1	demo_partner_conversion_in	demo_partner_conversion_out	x12	856004010			t	1	P	1			us-ascii	0	f	application/X12	\N	2026-10-11 16:52:26.804196	f	f		0	x12				0		0	0	0	
19	3	1	0	0	18	demo_partner_conversion	outcommunicate									f	1						0	f	text/plain	\N	2026-10-11 16:52:28.036486	f	f		0					0		0	0	0	
18	3	1	0	0	5	demo_partner_conversion	run				demo_partner_conversion_out					f	1						0	f	text/plain	\N	2026-10-11 16:52:27.790042	f	f		0					0		0	0	0	
5	3	1	0	0	4	demo_partner_conversion	routepart									f	1						0	f	text/plain	\N	2026-10-11 16:51:50.678223	f	f		0					0		0	0	0	
4	3	1	0	0	3	demo_partner_conversion	router									f	1						0	f	text/plain	\N	2026-10-11 16:51:50.348845	f	f		0					0		0	0	0	
35	3	220	26	0	33	inbound_orders	35			inbound_orders_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-11 16:53:00.906397	f	f		0					0		0	286	0	
27	3	200	0	0	24	inbound_orders	/o/pg/bots/botssys/infile/edifact_xml/edifact/0T0000000015.edi			inbound_orders_in						f	1						0	f	text/plain	\N	2026-10-11 16:52:43.992816	f	f		0					0		0	0	0	
29	3	200	0	0	24	inbound_orders	/o/pg/bots/botssys/infile/edifact_xml/edifact/T0000000001.edi			inbound_orders_in						f	1						0	f	text/plain	\N	2026-10-11 16:52:48.191659	f	f		0					0		0	0	0	
36	3	220	28	0	33	inbound_orders	36			inbound_orders_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-11 16:53:03.255713	f	f		0					0		0	261	0	
31	3	200	0	0	24	inbound_orders	/o/pg/bots/botssys/infile/edifact_xml/edifact/T0000000002.edi			inbound_orders_in						f	1						0	f	text/plain	\N	2026-10-11 16:52:49.885223	f	f		0					0		0	0	0	
24	3	1	0	0	23	inbound_orders	incommunicate									f	1						0	f	text/plain	\N	2026-10-11 16:52:40.139293	f	f		0					0		0	0	0	
23	3	1	0	0	22	inbound_orders	run			inbound_orders_in						f	1						0	f	text/plain	\N	2026-10-11 16:52:38.757712	f	f		0					0		0	0	0	
33	3	1	0	0	22	inbound_orders	preprocess									f	1						0	f	text/plain	\N	2026-10-11 16:52:58.929817	f	f		0					0		0	0	0	
26	3	220	25	0	24	inbound_orders	26			inbound_orders_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-11 16:52:41.555977	f	f		0					0		0	779	0	
37	3	220	30	0	33	inbound_orders	37			inbound_orders_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-11 16:53:04.281	f	f		0					0		0	276	0	
28	3	220	27	0	24	inbound_orders	28			inbound_orders_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-11 16:52:46.527966	f	f		0					0		0	262	0	
38	3	220	32	0	33	inbound_orders	38			inbound_orders_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-11 16:53:05.629559	f	f		0					0		0	282	0	
30	3	220	29	0	24	inbound_orders	30			inbound_orders_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-11 16:52:48.481045	f	f		0					0		0	278	0	
39	3	1	0	0	22	inbound_orders	translate									f	1						0	f	text/plain	\N	2026-10-11 16:53:11.704388	f	f		0					0		0	0	0	
32	3	220	31	0	24	inbound_orders	32			inbound_orders_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-11 16:52:50.568574	f	f		0					0		0	284	0	
22	3	1	0	0	21	inbound_orders	routepart									f	1						0	f	text/plain	\N	2026-10-11 16:52:37.841509	f	f		0					0		0	0	0	
21	3	1	0	0	3	inbound_orders	router									f	1						0	f	text/plain	\N	2026-10-11 16:52:36.954154	f	f		0					0		0	0	0	
3	3	1	0	0	0		rundispatcher									f	1						0	f	text/plain	\N	2026-10-11 16:51:49.853206	f	f		0					0		0	0	0	
66	3	500	58	0	22	inbound_orders	44	PARTNER1	PARTNER2	inbound_orders_in	inbound_orders_out	xml	orders			f	1		T0000000004-2			utf-8	0	f	text/xml 	\N	2026-10-11 16:53:51.972382	f	f		0					0		0	0	0	
41	3	320	40	0	39	inbound_orders	34	PARTNER1	PARTNER2	inbound_orders_in		edifact	ORDERSD96AUNEAN008		orders_edifact2xml	t	1		T0000000004-1			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:53:19.804867	f	f		0	edifact				0		0	0	0	
53	3	330	52	0	39	inbound_orders	53	PARTNER1	PARTNER2	inbound_orders_in		xml	orders		orders_edifact2xml	f	1		T0000000001			utf-8	0	f	text/xml 	\N	2026-10-11 16:53:37.948139	f	f		0					0		0	584	0	
43	3	320	40	0	39	inbound_orders	34	PARTNER1	PARTNER2	inbound_orders_in		edifact	ORDERSD96AUNEAN008		orders_edifact2xml	t	1		T0000000004-2			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:53:25.829285	f	f		0	edifact				0		0	0	0	
40	3	310	34	0	39	inbound_orders	34	PARTNER1	PARTNER2	inbound_orders_in		edifact	edifact			t	1					UNOA	0	f	application/EDIFACT	\N	2026-10-11 16:53:12.494658	f	f		0	edifact				0		0	489	0	
34	3	220	26	0	33	inbound_orders	34			inbound_orders_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-11 16:52:59.200466	f	f		0					0		0	489	0	
46	3	320	45	0	39	inbound_orders	35	PARTNER1	PARTNER2	inbound_orders_in		edifact	ORDERSD96AUNEAN008		orders_edifact2xml	t	1		T0000000004-3			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:53:28.193128	f	f		0	edifact				0		0	0	0	
45	3	310	35	0	39	inbound_orders	35	PARTNER1	PARTNER2	inbound_orders_in		edifact	edifact			t	1					UNOA	0	f	application/EDIFACT	\N	2026-10-11 16:53:28.028318	f	f		0	edifact				0		0	286	0	
57	3	400	42	0	22	inbound_orders	42	PARTNER1	PARTNER2	inbound_orders_in		xml	orders			f	1		T0000000004-1			utf-8	0	f	text/xml 	\N	2026-10-11 16:53:44.239596	f	f		0					0		0	586	0	
49	3	320	48	0	39	inbound_orders	36	PARTNER1	PARTNER2	inbound_orders_in		edifact	ORDERSD96AUNEAN008		orders_edifact2xml	t	1		T0000000015			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:53:31.098789	f	f		0	edifact				0		0	0	0	
48	3	310	36	0	39	inbound_orders	36	PARTNER1	PARTNER2	inbound_orders_in		edifact	edifact			t	1					UNOA	0	f	application/EDIFACT	\N	2026-10-11 16:53:30.783471	f	f		0	edifact				0		0	261	0	
42	3	330	41	0	39	inbound_orders	42	PARTNER1	PARTNER2	inbound_orders_in		xml	orders		orders_edifact2xml	f	1		T0000000004-1			utf-8	0	f	text/xml 	\N	2026-10-11 16:53:20.259086	f	f		0					0		0	586	0	
61	3	400	53	0	22	inbound_orders	53	PARTNER1	PARTNER2	inbound_orders_in		xml	orders			f	1		T0000000001			utf-8	0	f	text/xml 	\N	2026-10-11 16:53:47.825106	f	f		0					0		0	584	0	
52	3	320	51	0	39	inbound_orders	37	PARTNER1	PARTNER2	inbound_orders_in		edifact	ORDERSD96AUNEAN008		orders_edifact2xml	t	1		T0000000001			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:53:36.896635	f	f		0	edifact				0		0	0	0	
51	3	310	37	0	39	inbound_orders	37	PARTNER1	PARTNER2	inbound_orders_in		edifact	edifact			t	1					UNOA	0	f	application/EDIFACT	\N	2026-10-11 16:53:35.820605	f	f		0	edifact				0		0	276	0	
55	3	320	54	0	39	inbound_orders	38	PARTNER1	PARTNER2	inbound_orders_in		edifact	ORDERSD96AUNEAN008		orders_edifact2xml	t	1		T0000000002-1			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:53:40.727458	f	f		0	edifact				0		0	0	0	
54	3	310	38	0	39	inbound_orders	38	PARTNER1	PARTNER2	inbound_orders_in		edifact	edifact			t	1					UNOA	0	f	application/EDIFACT	\N	2026-10-11 16:53:40.391828	f	f		0	edifact				0		0	282	0	
67	3	500	59	0	22	inbound_orders	47	PARTNER1	PARTNER2	inbound_orders_in	inbound_orders_out	xml	orders			f	1		T0000000004-3			utf-8	0	f	text/xml 	\N	2026-10-11 16:53:56.927773	f	f		0					0		0	0	0	
44	3	330	43	0	39	inbound_orders	44	PARTNER1	PARTNER2	inbound_orders_in		xml	orders		orders_edifact2xml	f	1		T0000000004-2			utf-8	0	f	text/xml 	\N	2026-10-11 16:53:26.531172	f	f		0					0		0	586	0	
47	3	330	46	0	39	inbound_orders	47	PARTNER1	PARTNER2	inbound_orders_in		xml	orders		orders_edifact2xml	f	1		T0000000004-3			utf-8	0	f	text/xml 	\N	2026-10-11 16:53:29.000309	f	f		0					0		0	586	0	
50	3	330	49	0	39	inbound_orders	50	PARTNER1	PARTNER2	inbound_orders_in		xml	orders		orders_edifact2xml	f	1		T0000000015			utf-8	0	f	text/xml 	\N	2026-10-11 16:53:31.517546	f	f		0					0		0	584	0	
56	3	330	55	0	39	inbound_orders	56	PARTNER1	PARTNER2	inbound_orders_in		xml	orders		orders_edifact2xml	f	1		T0000000002-1			utf-8	0	f	text/xml 	\N	2026-10-11 16:53:41.169435	f	f		0					0		0	586	0	
64	3	500	62	0	22	inbound_orders	56	PARTNER1	PARTNER2	inbound_orders_in	inbound_orders_out	xml	orders			f	1		T0000000002-1			utf-8	0	f	text/xml 	\N	2026-10-11 16:53:50.525334	f	f		0					0		0	0	0	
65	3	500	57	0	22	inbound_orders	42	PARTNER1	PARTNER2	inbound_orders_in	inbound_orders_out	xml	orders			f	1		T0000000004-1			utf-8	0	f	text/xml 	\N	2026-10-11 16:53:51.207892	f	f		0					0		0	0	0	
62	3	400	56	0	22	inbound_orders	56	PARTNER1	PARTNER2	inbound_orders_in		xml	orders			f	1		T0000000002-1			utf-8	0	f	text/xml 	\N	2026-10-11 16:53:48.608545	f	f		0					0		0	586	0	
58	3	400	44	0	22	inbound_orders	44	PARTNER1	PARTNER2	inbound_orders_in		xml	orders			f	1		T0000000004-2			utf-8	0	f	text/xml 	\N	2026-10-11 16:53:45.863287	f	f		0					0		0	586	0	
68	3	500	60	0	22	inbound_orders	50	PARTNER1	PARTNER2	inbound_orders_in	inbound_orders_out	xml	orders			f	1		T0000000015			utf-8	0	f	text/xml 	\N	2026-10-11 16:53:57.480455	f	f		0					0		0	0	0	
59	3	400	47	0	22	inbound_orders	47	PARTNER1	PARTNER2	inbound_orders_in		xml	orders			f	1		T0000000004-3			utf-8	0	f	text/xml 	\N	2026-10-11 16:53:46.293246	f	f		0					0		0	586	0	
70	3	1	0	0	69	inbound_orders	outcommunicate									f	1						0	f	text/plain	\N	2026-10-11 16:54:00.096409	f	f		0					0		0	0	0	
60	3	400	50	0	22	inbound_orders	50	PARTNER1	PARTNER2	inbound_orders_in		xml	orders			f	1		T0000000015			utf-8	0	f	text/xml 	\N	2026-10-11 16:53:47.284456	f	f		0					0		0	584	0	
63	3	500	61	0	22	inbound_orders	53	PARTNER1	PARTNER2	inbound_orders_in	inbound_orders_out	xml	orders			f	1		T0000000001			utf-8	0	f	text/xml 	\N	2026-10-11 16:53:49.488921	f	f		0					0		0	0	0	
69	3	1	0	0	22	inbound_orders	run				inbound_orders_out					f	1						0	f	text/plain	\N	2026-10-11 16:53:58.395702	f	f		0					0		0	0	0	
71	3	520	63	0	70	inbound_orders	/o/pg/bots/botssys/outfile/edifact_xml/xml/orders_1.xml	PARTNER1	PARTNER2	inbound_orders_in	inbound_orders_out	xml	orders			f	1		T0000000001			utf-8	0	f	text/xml 	\N	2026-10-11 16:54:00.442614	f	f		0					0		0	0	1	
72	3	520	64	0	70	inbound_orders	/o/pg/bots/botssys/outfile/edifact_xml/xml/orders_2.xml	PARTNER1	PARTNER2	inbound_orders_in	inbound_orders_out	xml	orders			f	1		T0000000002-1			utf-8	0	f	text/xml 	\N	2026-10-11 16:54:01.412143	f	f		0					0		0	0	1	
73	3	520	65	0	70	inbound_orders	/o/pg/bots/botssys/outfile/edifact_xml/xml/orders_3.xml	PARTNER1	PARTNER2	inbound_orders_in	inbound_orders_out	xml	orders			f	1		T0000000004-1			utf-8	0	f	text/xml 	\N	2026-10-11 16:54:02.200363	f	f		0					0		0	0	1	
74	3	520	66	0	70	inbound_orders	/o/pg/bots/botssys/outfile/edifact_xml/xml/orders_4.xml	PARTNER1	PARTNER2	inbound_orders_in	inbound_orders_out	xml	orders			f	1		T0000000004-2			utf-8	0	f	text/xml 	\N	2026-10-11 16:54:03.132168	f	f		0					0		0	0	1	
75	3	520	67	0	70	inbound_orders	/o/pg/bots/botssys/outfile/edifact_xml/xml/orders_5.xml	PARTNER1	PARTNER2	inbound_orders_in	inbound_orders_out	xml	orders			f	1		T0000000004-3			utf-8	0	f	text/xml 	\N	2026-10-11 16:54:04.830048	f	f		0					0		0	0	1	
76	3	520	68	0	70	inbound_orders	/o/pg/bots/botssys/outfile/edifact_xml/xml/orders_6.xml	PARTNER1	PARTNER2	inbound_orders_in	inbound_orders_out	xml	orders			f	1		T0000000015			utf-8	0	f	text/xml 	\N	2026-10-11 16:54:05.407512	f	f		0					0		0	0	1	
81	3	200	0	0	80	myfirstroute	/o/pg/bots/botssys/infile/my_first_plugin/order01.edi			myfirstroute_in						f	1						0	f	text/plain	\N	2026-10-11 16:54:16.873824	f	f		0					0		0	0	0	
83	3	200	0	0	80	myfirstroute	/o/pg/bots/botssys/infile/my_first_plugin/order02.edi			myfirstroute_in						f	1						0	f	text/plain	\N	2026-10-11 16:54:19.614246	f	f		0					0		0	0	0	
85	3	200	0	0	80	myfirstroute	/o/pg/bots/botssys/infile/my_first_plugin/order03.edi			myfirstroute_in						f	1						0	f	text/plain	\N	2026-10-11 16:54:22.240475	f	f		0					0		0	0	0	
80	3	1	0	0	79	myfirstroute	incommunicate									f	1						0	f	text/plain	\N	2026-10-11 16:54:16.613385	f	f		0					0		0	0	0	
79	3	1	0	0	78	myfirstroute	run			myfirstroute_in						f	1						0	f	text/plain	\N	2026-10-11 16:54:13.472418	f	f		0					0		0	0	0	
94	3	320	93	0	92	myfirstroute	88	8712345678906	PARTNER2	myfirstroute_in		edifact	ORDERSD96AUNEAN008		orders_edifact2xml	t	1		T0000000004-1			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:54:34.79092	f	f		0	edifact				0		0	0	0	
82	3	220	81	0	80	myfirstroute	82			myfirstroute_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-11 16:54:17.284744	f	f		0					0		0	920	0	
84	3	220	83	0	80	myfirstroute	84			myfirstroute_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-11 16:54:20.665264	f	f		0					0		0	270	0	
92	3	1	0	0	78	myfirstroute	translate									f	1						0	f	text/plain	\N	2026-10-11 16:54:32.551841	f	f		0					0		0	0	0	
86	3	220	85	0	80	myfirstroute	86			myfirstroute_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-11 16:54:22.607476	f	f		0					0		0	267	0	
87	3	1	0	0	78	myfirstroute	preprocess									f	1						0	f	text/plain	\N	2026-10-11 16:54:26.585702	f	f		0					0		0	0	0	
96	3	320	93	0	92	myfirstroute	88	8712345678906	PARTNER2	myfirstroute_in		edifact	ORDERSD96AUNEAN008		orders_edifact2xml	t	1		T0000000004-2			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:54:37.305086	f	f		0	edifact				0		0	0	0	
93	3	310	88	0	92	myfirstroute	88	8712345678906	PARTNER2	myfirstroute_in		edifact	edifact			t	1					UNOA	0	f	application/EDIFACT	\N	2026-10-11 16:54:33.767425	f	f		0	edifact				0		0	500	0	
88	3	220	82	0	87	myfirstroute	88			myfirstroute_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-11 16:54:26.907289	f	f		0					0		0	500	0	
98	3	310	89	0	92	myfirstroute	89	8712345678906	PARTNER2	myfirstroute_in		edifact	edifact			t	1					UNOA	0	f	application/EDIFACT	\N	2026-10-11 16:54:39.613242	f	f		0	edifact				0		0	416	0	
99	3	320	98	0	92	myfirstroute	89	8712345678906	PARTNER2	myfirstroute_in		edifact	ORDERSD96AUNEAN008		orders_edifact2xml	t	1		T0000000004-3			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:54:39.78675	f	f		0	edifact				0		0	0	0	
89	3	220	82	0	87	myfirstroute	89			myfirstroute_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-11 16:54:27.89098	f	f		0					0		0	416	0	
102	3	320	101	0	92	myfirstroute	90	8712345678906	PARTNER2	myfirstroute_in		edifact	ORDERSD96AUNEAN008		orders_edifact2xml	t	1		T0000000015			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:54:42.031587	f	f		0	edifact				0		0	0	0	
101	3	310	90	0	92	myfirstroute	90	8712345678906	PARTNER2	myfirstroute_in		edifact	edifact			t	1					UNOA	0	f	application/EDIFACT	\N	2026-10-11 16:54:41.633372	f	f		0	edifact				0		0	269	0	
90	3	220	84	0	87	myfirstroute	90			myfirstroute_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-11 16:54:28.801311	f	f		0					0		0	269	0	
91	3	220	86	0	87	myfirstroute	91			myfirstroute_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-11 16:54:30.186055	f	f		0					0		0	265	0	
95	3	330	94	0	92	myfirstroute	95	8712345678906	PARTNER2	myfirstroute_in		xml	orders		orders_edifact2xml	f	1		ORDT0000000004-1			utf-8	0	f	text/xml 	\N	2026-10-11 16:54:35.728461	f	f		0					0		0	594	0	
97	3	330	96	0	92	myfirstroute	97	8712345678906	PARTNER2	myfirstroute_in		xml	orders		orders_edifact2xml	f	1		ORDT0000000004-2			utf-8	0	f	text/xml 	\N	2026-10-11 16:54:37.516265	f	f		0					0		0	594	0	
100	3	330	99	0	92	myfirstroute	100	8712345678906	PARTNER2	myfirstroute_in		xml	orders		orders_edifact2xml	f	1		ORDT0000000004-3			utf-8	0	f	text/xml 	\N	2026-10-11 16:54:39.85647	f	f		0					0		0	1006	0	
103	3	330	102	0	92	myfirstroute	103	8712345678906	PARTNER2	myfirstroute_in		xml	orders		orders_edifact2xml	f	1		ORDT0000000015			utf-8	0	f	text/xml 	\N	2026-10-11 16:54:42.540747	f	f		0					0		0	592	0	
78	3	1	0	0	77	myfirstroute	routepart									f	1						0	f	text/plain	\N	2026-10-11 16:54:08.187362	f	f		0					0		0	0	0	
77	3	1	0	0	3	myfirstroute	router									f	1						0	f	text/plain	\N	2026-10-11 16:54:07.65909	f	f		0					0		0	0	0	
105	3	320	104	0	92	myfirstroute	91	8712345678906	PARTNER2	myfirstroute_in		edifact	ORDERSD96AUNEAN008		orders_edifact2xml	t	1		T0000000001			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:54:46.003342	f	f		0	edifact				0		0	0	0	
104	3	310	91	0	92	myfirstroute	91	8712345678906	PARTNER2	myfirstroute_in		edifact	edifact			t	1					UNOA	0	f	application/EDIFACT	\N	2026-10-11 16:54:45.86311	f	f		0	edifact				0		0	265	0	
119	3	520	112	0	118	myfirstroute	/o/pg/bots/botssys/outfile/my_first_plugin/orders1.inh	8712345678906	PARTNER2	myfirstroute_in	myfirstroute_out	xml	orders			f	1		ORDT0000000004-1			utf-8	0	f	text/xml 	\N	2026-10-11 16:54:57.333217	f	f		0					0		0	0	1	
112	3	500	107	0	78	myfirstroute	95	8712345678906	PARTNER2	myfirstroute_in	myfirstroute_out	xml	orders			f	1		ORDT0000000004-1			utf-8	0	f	text/xml 	\N	2026-10-11 16:54:51.448156	f	f		0					0		0	0	0	
106	3	330	105	0	92	myfirstroute	106	8712345678906	PARTNER2	myfirstroute_in		xml	orders		orders_edifact2xml	f	1		ORDT0000000001			utf-8	0	f	text/xml 	\N	2026-10-11 16:54:46.496386	f	f		0					0		0	592	0	
116	3	500	111	0	78	myfirstroute	106	8712345678906	PARTNER2	myfirstroute_in	myfirstroute_out	xml	orders			f	1		ORDT0000000001			utf-8	0	f	text/xml 	\N	2026-10-11 16:54:55.989627	f	f		0					0		0	0	0	
107	3	400	95	0	78	myfirstroute	95	8712345678906	PARTNER2	myfirstroute_in		xml	orders			f	1		ORDT0000000004-1			utf-8	0	f	text/xml 	\N	2026-10-11 16:54:48.59185	f	f		0					0		0	594	0	
118	3	1	0	0	117	myfirstroute	outcommunicate									f	1						0	f	text/plain	\N	2026-10-11 16:54:57.198747	f	f		0					0		0	0	0	
108	3	400	97	0	78	myfirstroute	97	8712345678906	PARTNER2	myfirstroute_in		xml	orders			f	1		ORDT0000000004-2			utf-8	0	f	text/xml 	\N	2026-10-11 16:54:49.274773	f	f		0					0		0	594	0	
117	3	1	0	0	78	myfirstroute	run				myfirstroute_out					f	1						0	f	text/plain	\N	2026-10-11 16:54:56.379722	f	f		0					0		0	0	0	
109	3	400	100	0	78	myfirstroute	100	8712345678906	PARTNER2	myfirstroute_in		xml	orders			f	1		ORDT0000000004-3			utf-8	0	f	text/xml 	\N	2026-10-11 16:54:49.762431	f	f		0					0		0	1006	0	
110	3	400	103	0	78	myfirstroute	103	8712345678906	PARTNER2	myfirstroute_in		xml	orders			f	1		ORDT0000000015			utf-8	0	f	text/xml 	\N	2026-10-11 16:54:50.252534	f	f		0					0		0	592	0	
131	3	220	130	0	127	outbound_asn	131			outbound_asn_in		xml	asn			f	1						0	f	text/plain	\N	2026-10-11 16:55:08.323297	f	f		0					0		0	4523	0	
111	3	400	106	0	78	myfirstroute	106	8712345678906	PARTNER2	myfirstroute_in		xml	orders			f	1		ORDT0000000001			utf-8	0	f	text/xml 	\N	2026-10-11 16:54:50.837804	f	f		0					0		0	592	0	
120	3	520	113	0	118	myfirstroute	/o/pg/bots/botssys/outfile/my_first_plugin/orders2.inh	8712345678906	PARTNER2	myfirstroute_in	myfirstroute_out	xml	orders			f	1		ORDT0000000004-2			utf-8	0	f	text/xml 	\N	2026-10-11 16:54:58.51061	f	f		0					0		0	0	1	
113	3	500	108	0	78	myfirstroute	97	8712345678906	PARTNER2	myfirstroute_in	myfirstroute_out	xml	orders			f	1		ORDT0000000004-2			utf-8	0	f	text/xml 	\N	2026-10-11 16:54:53.064551	f	f		0					0		0	0	0	
121	3	520	114	0	118	myfirstroute	/o/pg/bots/botssys/outfile/my_first_plugin/orders3.inh	8712345678906	PARTNER2	myfirstroute_in	myfirstroute_out	xml	orders			f	1		ORDT0000000004-3			utf-8	0	f	text/xml 	\N	2026-10-11 16:54:59.909116	f	f		0					0		0	0	1	
114	3	500	109	0	78	myfirstroute	100	8712345678906	PARTNER2	myfirstroute_in	myfirstroute_out	xml	orders			f	1		ORDT0000000004-3			utf-8	0	f	text/xml 	\N	2026-10-11 16:54:53.687641	f	f		0					0		0	0	0	
122	3	520	115	0	118	myfirstroute	/o/pg/bots/botssys/outfile/my_first_plugin/orders4.inh	8712345678906	PARTNER2	myfirstroute_in	myfirstroute_out	xml	orders			f	1		ORDT0000000015			utf-8	0	f	text/xml 	\N	2026-10-11 16:55:01.538857	f	f		0					0		0	0	1	
115	3	500	110	0	78	myfirstroute	103	8712345678906	PARTNER2	myfirstroute_in	myfirstroute_out	xml	orders			f	1		ORDT0000000015			utf-8	0	f	text/xml 	\N	2026-10-11 16:54:54.358665	f	f		0					0		0	0	0	
123	3	520	116	0	118	myfirstroute	/o/pg/bots/botssys/outfile/my_first_plugin/orders5.inh	8712345678906	PARTNER2	myfirstroute_in	myfirstroute_out	xml	orders			f	1		ORDT0000000001			utf-8	0	f	text/xml 	\N	2026-10-11 16:55:03.008649	f	f		0					0		0	0	1	
129	3	220	128	0	127	outbound_asn	129			outbound_asn_in		xml	asn			f	1						0	f	text/plain	\N	2026-10-11 16:55:07.731536	f	f		0					0		0	16468	0	
133	3	220	132	0	127	outbound_asn	133			outbound_asn_in		xml	asn			f	1						0	f	text/plain	\N	2026-10-11 16:55:08.811369	f	f		0					0		0	1192	0	
128	3	200	0	0	127	outbound_asn	/o/pg/bots/botssys/infile/demo_work_with_partners/asn/856_PARTNER1_03.xml			outbound_asn_in						f	1						0	f	text/plain	\N	2026-10-11 16:55:07.479252	f	f		0					0		0	0	0	
130	3	200	0	0	127	outbound_asn	/o/pg/bots/botssys/infile/demo_work_with_partners/asn/856_PARTNER2_01.xml			outbound_asn_in						f	1						0	f	text/plain	\N	2026-10-11 16:55:08.199825	f	f		0					0		0	0	0	
125	3	1	0	0	124	outbound_asn	routepart									f	1						0	f	text/plain	\N	2026-10-11 16:55:06.497821	f	f		0					0		0	0	0	
132	3	200	0	0	127	outbound_asn	/o/pg/bots/botssys/infile/demo_work_with_partners/asn/856_PARTNER2_04.xml			outbound_asn_in						f	1						0	f	text/plain	\N	2026-10-11 16:55:08.624136	f	f		0					0		0	0	0	
519	3	330	518	536	513	outbound_invoice	519	SENDER	RECEIVER	outbound_invoice_in		edifact	INVOICD96AUNEAN008		invoice_xml2edifact	t	1		54			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:35.994453	f	f		0	edifact				0		0	744	0	
124	3	1	0	0	3	outbound_asn	router									f	1						0	f	text/plain	\N	2026-10-11 16:55:06.283701	f	f		0					0		0	0	0	
134	3	200	0	0	127	outbound_asn	/o/pg/bots/botssys/infile/demo_work_with_partners/asn/856_PARTNER3_02.xml			outbound_asn_in						f	1						0	f	text/plain	\N	2026-10-11 16:55:09.056136	f	f		0					0		0	0	0	
127	3	1	0	0	126	outbound_asn	incommunicate									f	1						0	f	text/plain	\N	2026-10-11 16:55:07.377729	f	f		0					0		0	0	0	
126	3	1	0	0	125	outbound_asn	run			outbound_asn_in						f	1						0	f	text/plain	\N	2026-10-11 16:55:06.749779	f	f		0					0		0	0	0	
518	3	320	517	0	513	outbound_invoice	504	SENDER	RECEIVER	outbound_invoice_in		xml	invoice		invoice_xml2edifact	f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:59:35.645452	f	f		0					0		0	0	0	
517	3	310	504	0	513	outbound_invoice	504	SENDER	RECEIVER	outbound_invoice_in		xml	invoice			f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:59:35.55575	f	f		0					0		0	2196	0	
138	3	320	137	0	136	outbound_asn	131	SENDER	PARTNER2	outbound_asn_in		xml	asn		asn_xml2x12_partner2	f	1	P				utf-8	0	f	text/xml 	\N	2026-10-11 16:55:10.572835	f	f		0					0		0	0	0	
137	3	310	131	0	136	outbound_asn	131	SENDER	PARTNER2	outbound_asn_in		xml	asn			f	1	P				utf-8	0	f	text/xml 	\N	2026-10-11 16:55:10.258709	f	f		0					0		0	4523	0	
142	3	330	141	149	136	outbound_asn	142	SENDER	PARTNER1	outbound_asn_in		x12	856004010		asn_xml2x12_default	t	1	P	14			us-ascii	0	f	application/X12	\N	2026-10-11 16:55:12.636754	f	f		0	x12				0		0	4056	0	
141	3	320	140	0	136	outbound_asn	129	SENDER	PARTNER1	outbound_asn_in		xml	asn		asn_xml2x12_default	f	1	P				utf-8	0	f	text/xml 	\N	2026-10-11 16:55:12.478656	f	f		0					0		0	0	0	
140	3	310	129	0	136	outbound_asn	129	SENDER	PARTNER1	outbound_asn_in		xml	asn			f	1	P				utf-8	0	f	text/xml 	\N	2026-10-11 16:55:12.370691	f	f		0					0		0	16468	0	
144	3	320	143	0	136	outbound_asn	133	SENDER	PARTNER2	outbound_asn_in		xml	asn		asn_xml2x12_partner2	f	1	P				utf-8	0	f	text/xml 	\N	2026-10-11 16:55:13.56277	f	f		0					0		0	0	0	
143	3	310	133	0	136	outbound_asn	133	SENDER	PARTNER2	outbound_asn_in		xml	asn			f	1	P				utf-8	0	f	text/xml 	\N	2026-10-11 16:55:13.301835	f	f		0					0		0	1192	0	
139	3	330	138	150	136	outbound_asn	139	SENDER	PARTNER2	outbound_asn_in		x12	856004010		asn_xml2x12_partner2	t	1	P	13			us-ascii	0	f	application/X12	\N	2026-10-11 16:55:10.932984	f	f		0	x12				0		0	1603	0	
145	3	330	144	150	136	outbound_asn	145	SENDER	PARTNER2	outbound_asn_in		x12	856004010		asn_xml2x12_partner2	t	1	P	15			us-ascii	0	f	application/X12	\N	2026-10-11 16:55:13.841354	f	f		0	x12				0		0	430	0	
147	3	320	146	0	136	outbound_asn	135	SENDER	PARTNER3	outbound_asn_in		xml	asn		asn_xml2x12_noSSCC	f	1	P				utf-8	0	f	text/xml 	\N	2026-10-11 16:55:16.243246	f	f		0					0		0	0	0	
146	3	310	135	0	136	outbound_asn	135	SENDER	PARTNER3	outbound_asn_in		xml	asn			f	1	P				utf-8	0	f	text/xml 	\N	2026-10-11 16:55:16.039816	f	f		0					0		0	3396	0	
135	3	220	134	0	127	outbound_asn	135			outbound_asn_in		xml	asn			f	1						0	f	text/plain	\N	2026-10-11 16:55:09.235287	f	f		0					0		0	3396	0	
136	3	1	0	0	125	outbound_asn	translate									f	1						0	f	text/plain	\N	2026-10-11 16:55:10.193256	f	f		0					0		0	0	0	
148	3	330	147	151	136	outbound_asn	148	SENDER	PARTNER3	outbound_asn_in		x12	856004010		asn_xml2x12_noSSCC	t	1	P	16			us-ascii	0	f	application/X12	\N	2026-10-11 16:55:16.59061	f	f		0	x12				0		0	1037	0	
151	3	400	0	0	125	outbound_asn	151	SENDER	PARTNER3	outbound_asn_in		x12	856004010			t	1	P	3			us-ascii	0	f	application/X12	\N	2026-10-11 16:55:20.921128	f	f		0	x12				0		0	1219	0	
161	3	520	158	0	160	outbound_asn	/o/pg/bots/botssys/outfile/demo_work_with_partners/outbound_856/PARTNER2_20261011_1.x12	SENDER	PARTNER2	outbound_asn_in	outbound_asn_out_partner2	x12	856004010			t	2	P	2			us-ascii	0	f	application/X12	\N	2026-10-11 16:55:33.344303	f	f		0	x12				0		0	0	1	
156	3	520	153	0	155	outbound_asn	/o/pg/bots/botssys/outfile/demo_work_with_partners/outbound_856/PARTNER3_pgroupA_20261011_1.x12	SENDER	PARTNER3	outbound_asn_in	outbound_asn_out_pgroupA	x12	856004010			t	1	P	3			us-ascii	0	f	application/X12	\N	2026-10-11 16:55:28.120582	f	f		0	x12				0		0	0	1	
153	3	500	151	0	152	outbound_asn	151	SENDER	PARTNER3	outbound_asn_in	outbound_asn_out_pgroupA	x12	856004010			t	1	P	3			us-ascii	0	f	application/X12	\N	2026-10-11 16:55:24.768841	f	f		0	x12				0		0	0	0	
155	3	1	0	0	154	outbound_asn	outcommunicate									f	1						0	f	text/plain	\N	2026-10-11 16:55:27.041441	f	f		0					0		0	0	0	
154	3	1	0	0	152	outbound_asn	run				outbound_asn_out_pgroupA					f	1						0	f	text/plain	\N	2026-10-11 16:55:25.728759	f	f		0					0		0	0	0	
152	3	1	0	0	124	outbound_asn	routepart									f	1						0	f	text/plain	\N	2026-10-11 16:55:23.906057	f	f		0					0		0	0	0	
165	3	1	0	0	164	outbound_asn	outcommunicate									f	1						0	f	text/plain	\N	2026-10-11 16:55:48.341056	f	f		0					0		0	0	0	
150	3	400	0	0	125	outbound_asn	150	SENDER	PARTNER2	outbound_asn_in		x12	856004010			t	2	P	2			us-ascii	0	f	application/X12	\N	2026-10-11 16:55:19.906025	f	f		0	x12				0		0	2215	0	
149	3	400	0	0	125	outbound_asn	149	SENDER	PARTNER1	outbound_asn_in		x12	856004010			t	1	P	1			us-ascii	0	f	application/X12	\N	2026-10-11 16:55:18.414727	f	f		0	x12				0		0	4238	0	
158	3	500	150	0	157	outbound_asn	150	SENDER	PARTNER2	outbound_asn_in	outbound_asn_out_partner2	x12	856004010			t	2	P	2			us-ascii	0	f	application/X12	\N	2026-10-11 16:55:34.350069	f	f		0	x12				0		0	0	0	
160	3	1	0	0	159	outbound_asn	outcommunicate									f	1						0	f	text/plain	\N	2026-10-11 16:55:32.802535	f	f		0					0		0	0	0	
159	3	1	0	0	157	outbound_asn	run				outbound_asn_out_partner2					f	1						0	f	text/plain	\N	2026-10-11 16:55:32.319239	f	f		0					0		0	0	0	
157	3	1	0	0	124	outbound_asn	routepart									f	1						0	f	text/plain	\N	2026-10-11 16:55:32.401419	f	f		0					0		0	0	0	
162	3	1	0	0	124	outbound_asn	routepart									f	1						0	f	text/plain	\N	2026-10-11 16:55:36.573421	f	f		0					0		0	0	0	
166	3	520	163	0	165	outbound_asn	/o/pg/bots/botssys/outfile/demo_work_with_partners/outbound_856/PARTNER1_20261011_1.x12	SENDER	PARTNER1	outbound_asn_in	outbound_asn_out	x12	856004010			t	1	P	1			us-ascii	0	f	application/X12	\N	2026-10-11 16:55:48.624195	f	f		0	x12				0		0	0	1	
163	3	500	149	0	162	outbound_asn	149	SENDER	PARTNER1	outbound_asn_in	outbound_asn_out	x12	856004010			t	1	P	1			us-ascii	0	f	application/X12	\N	2026-10-11 16:55:36.700862	f	f		0	x12				0		0	0	0	
164	3	1	0	0	162	outbound_asn	run				outbound_asn_out					f	1						0	f	text/plain	\N	2026-10-11 16:55:38.488029	f	f		0					0		0	0	0	
168	3	1	0	0	167	outbound_desadv	routepart									f	1						0	f	text/plain	\N	2026-10-11 16:55:52.278696	f	f		0					0		0	0	0	
170	3	1	0	0	169	outbound_desadv	incommunicate									f	1						0	f	text/plain	\N	2026-10-11 16:55:55.390006	f	f		0					0		0	0	0	
169	3	1	0	0	168	outbound_desadv	run			outbound_desadv_in						f	1						0	f	text/plain	\N	2026-10-11 16:55:52.581374	f	f		0					0		0	0	0	
167	3	1	0	0	3	outbound_desadv	router									f	1						0	f	text/plain	\N	2026-10-11 16:55:51.693679	f	f		0					0		0	0	0	
171	3	200	0	0	170	outbound_desadv	/o/pg/bots/botssys/infile/edifact_xml/xml/desadv1923.xml			outbound_desadv_in						f	1						0	f	text/plain	\N	2026-10-11 16:56:01.016787	f	f		0					0		0	0	0	
173	3	200	0	0	170	outbound_desadv	/o/pg/bots/botssys/infile/edifact_xml/xml/desadvfull01.xml			outbound_desadv_in						f	1						0	f	text/plain	\N	2026-10-11 16:56:06.477223	f	f		0					0		0	0	0	
175	3	200	0	0	170	outbound_desadv	/o/pg/bots/botssys/infile/edifact_xml/xml/desadvtest01.xml			outbound_desadv_in						f	1						0	f	text/plain	\N	2026-10-11 16:56:08.006982	f	f		0					0		0	0	0	
177	3	200	0	0	170	outbound_desadv	/o/pg/bots/botssys/infile/edifact_xml/xml/desadvtest5-1.xml			outbound_desadv_in						f	1						0	f	text/plain	\N	2026-10-11 16:56:09.425171	f	f		0					0		0	0	0	
179	3	200	0	0	170	outbound_desadv	/o/pg/bots/botssys/infile/edifact_xml/xml/desadvtest5-2.xml			outbound_desadv_in						f	1						0	f	text/plain	\N	2026-10-11 16:56:09.800825	f	f		0					0		0	0	0	
181	3	200	0	0	170	outbound_desadv	/o/pg/bots/botssys/infile/edifact_xml/xml/desadvtest6-1.xml			outbound_desadv_in						f	1						0	f	text/plain	\N	2026-10-11 16:56:10.522718	f	f		0					0		0	0	0	
187	3	320	186	0	185	outbound_desadv	172	5555555555555	1111111111111	outbound_desadv_in		xml	desadv		desadv_xml2edifact	f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:56:14.435446	f	f		0					0		0	0	0	
183	3	200	0	0	170	outbound_desadv	/o/pg/bots/botssys/infile/edifact_xml/xml/desadvtest6-2.xml			outbound_desadv_in						f	1						0	f	text/plain	\N	2026-10-11 16:56:11.173876	f	f		0					0		0	0	0	
185	3	1	0	0	168	outbound_desadv	translate									f	1						0	f	text/plain	\N	2026-10-11 16:56:12.913827	f	f		0					0		0	0	0	
186	3	310	172	0	185	outbound_desadv	172	5555555555555	1111111111111	outbound_desadv_in		xml	desadv			f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:56:13.699313	f	f		0					0		0	1320	0	
172	3	220	171	0	170	outbound_desadv	172			outbound_desadv_in		xml	desadv			f	1						0	f	text/plain	\N	2026-10-11 16:56:01.370707	f	f		0					0		0	1320	0	
193	3	320	192	0	185	outbound_desadv	176	SENDER	RECEIVER	outbound_desadv_in		xml	desadv		desadv_xml2edifact	f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:56:18.845233	f	f		0					0		0	0	0	
190	3	320	189	0	185	outbound_desadv	174	5555555555555	1111111111111	outbound_desadv_in		xml	desadv		desadv_xml2edifact	f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:56:17.118781	f	f		0					0		0	0	0	
189	3	310	174	0	185	outbound_desadv	174	5555555555555	1111111111111	outbound_desadv_in		xml	desadv			f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:56:16.960336	f	f		0					0		0	11810	0	
174	3	220	173	0	170	outbound_desadv	174			outbound_desadv_in		xml	desadv			f	1						0	f	text/plain	\N	2026-10-11 16:56:06.558784	f	f		0					0		0	11810	0	
192	3	310	176	0	185	outbound_desadv	176	SENDER	RECEIVER	outbound_desadv_in		xml	desadv			f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:56:18.730966	f	f		0					0		0	1571	0	
176	3	220	175	0	170	outbound_desadv	176			outbound_desadv_in		xml	desadv			f	1						0	f	text/plain	\N	2026-10-11 16:56:08.657154	f	f		0					0		0	1571	0	
198	3	310	180	0	185	outbound_desadv	180	5555555555555	2222222222222	outbound_desadv_in		xml	desadv			f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:56:21.146666	f	f		0					0		0	1503	0	
196	3	320	195	0	185	outbound_desadv	178	5555555555555	1111111111111	outbound_desadv_in		xml	desadv		desadv_xml2edifact	f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:56:20.118293	f	f		0					0		0	0	0	
195	3	310	178	0	185	outbound_desadv	178	5555555555555	1111111111111	outbound_desadv_in		xml	desadv			f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:56:20.03967	f	f		0					0		0	1503	0	
178	3	220	177	0	170	outbound_desadv	178			outbound_desadv_in		xml	desadv			f	1						0	f	text/plain	\N	2026-10-11 16:56:09.4845	f	f		0					0		0	1503	0	
180	3	220	179	0	170	outbound_desadv	180			outbound_desadv_in		xml	desadv			f	1						0	f	text/plain	\N	2026-10-11 16:56:09.888586	f	f		0					0		0	1503	0	
199	3	320	198	0	185	outbound_desadv	180	5555555555555	2222222222222	outbound_desadv_in		xml	desadv		desadv_xml2edifact	f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:56:21.249712	f	f		0					0		0	0	0	
201	3	310	182	0	185	outbound_desadv	182	6666666666666	1111111111111	outbound_desadv_in		xml	desadv			f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:56:22.793113	f	f		0					0		0	1503	0	
202	3	320	201	0	185	outbound_desadv	182	6666666666666	1111111111111	outbound_desadv_in		xml	desadv		desadv_xml2edifact	f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:56:23.157658	f	f		0					0		0	0	0	
182	3	220	181	0	170	outbound_desadv	182			outbound_desadv_in		xml	desadv			f	1						0	f	text/plain	\N	2026-10-11 16:56:10.701228	f	f		0					0		0	1503	0	
184	3	220	183	0	170	outbound_desadv	184			outbound_desadv_in		xml	desadv			f	1						0	f	text/plain	\N	2026-10-11 16:56:11.273269	f	f		0					0		0	1503	0	
188	3	330	187	207	185	outbound_desadv	188	5555555555555	1111111111111	outbound_desadv_in		edifact	DESADVD96AUNEAN005		desadv_xml2edifact	t	1		17			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:56:14.834211	f	f		0	edifact				0		0	366	0	
191	3	330	190	207	185	outbound_desadv	191	5555555555555	1111111111111	outbound_desadv_in		edifact	DESADVD96AUNEAN005		desadv_xml2edifact	t	1		18			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:56:17.283477	f	f		0	edifact				0		0	2793	0	
197	3	330	196	207	185	outbound_desadv	197	5555555555555	1111111111111	outbound_desadv_in		edifact	DESADVD96AUNEAN005		desadv_xml2edifact	t	1		20			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:56:20.266243	f	f		0	edifact				0		0	495	0	
200	3	330	199	208	185	outbound_desadv	200	5555555555555	2222222222222	outbound_desadv_in		edifact	DESADVD96AUNEAN005		desadv_xml2edifact	t	1		21			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:56:21.436171	f	f		0	edifact				0		0	495	0	
203	3	330	202	209	185	outbound_desadv	203	6666666666666	1111111111111	outbound_desadv_in		edifact	DESADVD96AUNEAN005		desadv_xml2edifact	t	1		22			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:56:23.755101	f	f		0	edifact				0		0	495	0	
194	3	330	193	211	185	outbound_desadv	194	SENDER	RECEIVER	outbound_desadv_in		edifact	DESADVD96AUNEAN005		desadv_xml2edifact	t	1		19			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:56:19.085633	f	f		0	edifact				0		0	495	0	
217	3	1	0	0	168	outbound_desadv	run				outbound_desadv_out					f	1						0	f	text/plain	\N	2026-10-11 16:56:38.05814	f	f		0					0		0	0	0	
205	3	320	204	0	185	outbound_desadv	184	6666666666666	2222222222222	outbound_desadv_in		xml	desadv		desadv_xml2edifact	f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:56:25.515934	f	f		0					0		0	0	0	
204	3	310	184	0	185	outbound_desadv	184	6666666666666	2222222222222	outbound_desadv_in		xml	desadv			f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:56:25.112822	f	f		0					0		0	1503	0	
521	3	320	520	0	513	outbound_invoice	506	5555555555555	1111111111111	outbound_invoice_in		xml	invoice		invoice_xml2edifact	f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:59:36.739055	f	f		0					0		0	0	0	
551	3	1	0	0	550	demo_partner_conversion	routepart									f	1						0	f	text/plain	\N	2026-10-12 03:50:49.011097	f	f		0					0		0	0	0	
206	3	330	205	210	185	outbound_desadv	206	6666666666666	2222222222222	outbound_desadv_in		edifact	DESADVD96AUNEAN005		desadv_xml2edifact	t	1		23			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:56:25.795973	f	f		0	edifact				0		0	495	0	
207	3	400	0	0	168	outbound_desadv	207	5555555555555	1111111111111	outbound_desadv_in		edifact	DESADVD96AUNEAN005			t	3		1			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:56:27.067128	f	f		0	edifact				0		0	3736	0	
221	3	520	214	0	218	outbound_desadv	/o/pg/bots/botssys/outfile/edifact_xml/edifact/desadv3.edi	6666666666666	1111111111111	outbound_desadv_in	outbound_desadv_out	edifact	DESADVD96AUNEAN005			t	1		1			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:56:41.159797	f	f		0	edifact				0		0	0	1	
208	3	400	0	0	168	outbound_desadv	208	5555555555555	2222222222222	outbound_desadv_in		edifact	DESADVD96AUNEAN005			t	1		2			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:56:32.853065	f	f		0	edifact				0		0	577	0	
209	3	400	0	0	168	outbound_desadv	209	6666666666666	1111111111111	outbound_desadv_in		edifact	DESADVD96AUNEAN005			t	1		1			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:56:33.535058	f	f		0	edifact				0		0	577	0	
210	3	400	0	0	168	outbound_desadv	210	6666666666666	2222222222222	outbound_desadv_in		edifact	DESADVD96AUNEAN005			t	1		2			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:56:34.397839	f	f		0	edifact				0		0	577	0	
211	3	400	0	0	168	outbound_desadv	211	SENDER	RECEIVER	outbound_desadv_in		edifact	DESADVD96AUNEAN005			t	1		1			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:56:34.818087	f	f		0	edifact				0		0	565	0	
219	3	520	212	0	218	outbound_desadv	/o/pg/bots/botssys/outfile/edifact_xml/edifact/desadv1.edi	5555555555555	1111111111111	outbound_desadv_in	outbound_desadv_out	edifact	DESADVD96AUNEAN005			t	3		1			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:56:39.075646	f	f		0	edifact				0		0	0	1	
212	3	500	207	0	168	outbound_desadv	207	5555555555555	1111111111111	outbound_desadv_in	outbound_desadv_out	edifact	DESADVD96AUNEAN005			t	3		1			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:56:35.682954	f	f		0	edifact				0		0	0	0	
220	3	520	213	0	218	outbound_desadv	/o/pg/bots/botssys/outfile/edifact_xml/edifact/desadv2.edi	5555555555555	2222222222222	outbound_desadv_in	outbound_desadv_out	edifact	DESADVD96AUNEAN005			t	1		2			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:56:40.075545	f	f		0	edifact				0		0	0	1	
213	3	500	208	0	168	outbound_desadv	208	5555555555555	2222222222222	outbound_desadv_in	outbound_desadv_out	edifact	DESADVD96AUNEAN005			t	1		2			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:56:36.040799	f	f		0	edifact				0		0	0	0	
214	3	500	209	0	168	outbound_desadv	209	6666666666666	1111111111111	outbound_desadv_in	outbound_desadv_out	edifact	DESADVD96AUNEAN005			t	1		1			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:56:36.311526	f	f		0	edifact				0		0	0	0	
222	3	520	215	0	218	outbound_desadv	/o/pg/bots/botssys/outfile/edifact_xml/edifact/desadv4.edi	6666666666666	2222222222222	outbound_desadv_in	outbound_desadv_out	edifact	DESADVD96AUNEAN005			t	1		2			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:56:41.808699	f	f		0	edifact				0		0	0	1	
215	3	500	210	0	168	outbound_desadv	210	6666666666666	2222222222222	outbound_desadv_in	outbound_desadv_out	edifact	DESADVD96AUNEAN005			t	1		2			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:56:36.592779	f	f		0	edifact				0		0	0	0	
223	3	520	216	0	218	outbound_desadv	/o/pg/bots/botssys/outfile/edifact_xml/edifact/desadv5.edi	SENDER	RECEIVER	outbound_desadv_in	outbound_desadv_out	edifact	DESADVD96AUNEAN005			t	1		1			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:56:42.259115	f	f		0	edifact				0		0	0	1	
216	3	500	211	0	168	outbound_desadv	211	SENDER	RECEIVER	outbound_desadv_in	outbound_desadv_out	edifact	DESADVD96AUNEAN005			t	1		1			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:56:37.260794	f	f		0	edifact				0		0	0	0	
218	3	1	0	0	217	outbound_desadv	outcommunicate									f	1						0	f	text/plain	\N	2026-10-11 16:56:38.320078	f	f		0					0		0	0	0	
225	3	1	0	0	224	outbound_invoice	routepart									f	1						0	f	text/plain	\N	2026-10-11 16:56:43.471071	f	f		0					0		0	0	0	
229	3	220	228	0	227	outbound_invoice	229			outbound_invoice_in		xml	invoice			f	1						0	f	text/plain	\N	2026-10-11 16:56:45.022725	f	f		0					0		0	5539	0	
228	3	200	0	0	227	outbound_invoice	/o/pg/bots/botssys/infile/edifact_xml/xml/invoicfull01.xml			outbound_invoice_in						f	1						0	f	text/plain	\N	2026-10-11 16:56:44.92708	f	f		0					0		0	0	0	
224	3	1	0	0	3	outbound_invoice	router									f	1						0	f	text/plain	\N	2026-10-11 16:56:43.111583	f	f		0					0		0	0	0	
230	3	200	0	0	227	outbound_invoice	/o/pg/bots/botssys/infile/edifact_xml/xml/invoictest01.xml			outbound_invoice_in						f	1						0	f	text/plain	\N	2026-10-11 16:56:45.248535	f	f		0					0		0	0	0	
232	3	200	0	0	227	outbound_invoice	/o/pg/bots/botssys/infile/edifact_xml/xml/invoictest5-1.xml			outbound_invoice_in						f	1						0	f	text/plain	\N	2026-10-11 16:56:45.608677	f	f		0					0		0	0	0	
234	3	200	0	0	227	outbound_invoice	/o/pg/bots/botssys/infile/edifact_xml/xml/invoictest5-2.xml			outbound_invoice_in						f	1						0	f	text/plain	\N	2026-10-11 16:56:45.876759	f	f		0					0		0	0	0	
227	3	1	0	0	226	outbound_invoice	incommunicate									f	1						0	f	text/plain	\N	2026-10-11 16:56:44.831441	f	f		0					0		0	0	0	
226	3	1	0	0	225	outbound_invoice	run			outbound_invoice_in						f	1						0	f	text/plain	\N	2026-10-11 16:56:44.598039	f	f		0					0		0	0	0	
236	3	200	0	0	227	outbound_invoice	/o/pg/bots/botssys/infile/edifact_xml/xml/invoictest6-1.xml			outbound_invoice_in						f	1						0	f	text/plain	\N	2026-10-11 16:56:46.192444	f	f		0					0		0	0	0	
238	3	200	0	0	227	outbound_invoice	/o/pg/bots/botssys/infile/edifact_xml/xml/invoictest6-2.xml			outbound_invoice_in						f	1						0	f	text/plain	\N	2026-10-11 16:56:46.432567	f	f		0					0		0	0	0	
242	3	320	241	0	240	outbound_invoice	229	5555555555555	1111111111111	outbound_invoice_in		xml	invoice		invoice_xml2edifact	f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:56:47.780918	f	f		0					0		0	0	0	
241	3	310	229	0	240	outbound_invoice	229	5555555555555	1111111111111	outbound_invoice_in		xml	invoice			f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:56:47.429685	f	f		0					0		0	5539	0	
248	3	320	247	0	240	outbound_invoice	233	5555555555555	1111111111111	outbound_invoice_in		xml	invoice		invoice_xml2edifact	f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:56:52.386025	f	f		0					0		0	0	0	
247	3	310	233	0	240	outbound_invoice	233	5555555555555	1111111111111	outbound_invoice_in		xml	invoice			f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:56:52.25842	f	f		0					0		0	2208	0	
245	3	320	244	0	240	outbound_invoice	231	SENDER	RECEIVER	outbound_invoice_in		xml	invoice		invoice_xml2edifact	f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:56:50.54135	f	f		0					0		0	0	0	
244	3	310	231	0	240	outbound_invoice	231	SENDER	RECEIVER	outbound_invoice_in		xml	invoice			f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:56:50.015295	f	f		0					0		0	2196	0	
231	3	220	230	0	227	outbound_invoice	231			outbound_invoice_in		xml	invoice			f	1						0	f	text/plain	\N	2026-10-11 16:56:45.302456	f	f		0					0		0	2196	0	
233	3	220	232	0	227	outbound_invoice	233			outbound_invoice_in		xml	invoice			f	1						0	f	text/plain	\N	2026-10-11 16:56:45.697657	f	f		0					0		0	2208	0	
251	3	320	250	0	240	outbound_invoice	235	5555555555555	2222222222222	outbound_invoice_in		xml	invoice		invoice_xml2edifact	f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:56:53.877647	f	f		0					0		0	0	0	
250	3	310	235	0	240	outbound_invoice	235	5555555555555	2222222222222	outbound_invoice_in		xml	invoice			f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:56:53.5304	f	f		0					0		0	2208	0	
235	3	220	234	0	227	outbound_invoice	235			outbound_invoice_in		xml	invoice			f	1						0	f	text/plain	\N	2026-10-11 16:56:46.00442	f	f		0					0		0	2208	0	
254	3	320	253	0	240	outbound_invoice	237	6666666666666	1111111111111	outbound_invoice_in		xml	invoice		invoice_xml2edifact	f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:56:55.299879	f	f		0					0		0	0	0	
253	3	310	237	0	240	outbound_invoice	237	6666666666666	1111111111111	outbound_invoice_in		xml	invoice			f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:56:55.101019	f	f		0					0		0	2208	0	
237	3	220	236	0	227	outbound_invoice	237			outbound_invoice_in		xml	invoice			f	1						0	f	text/plain	\N	2026-10-11 16:56:46.243411	f	f		0					0		0	2208	0	
243	3	330	242	259	240	outbound_invoice	243	5555555555555	1111111111111	outbound_invoice_in		edifact	INVOICD96AUNEAN008		invoice_xml2edifact	t	1		24			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:56:47.951415	f	f		0	edifact				0		0	1579	0	
257	3	320	256	0	240	outbound_invoice	239	6666666666666	2222222222222	outbound_invoice_in		xml	invoice		invoice_xml2edifact	f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:56:56.154056	f	f		0					0		0	0	0	
256	3	310	239	0	240	outbound_invoice	239	6666666666666	2222222222222	outbound_invoice_in		xml	invoice			f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:56:56.042601	f	f		0					0		0	2208	0	
239	3	220	238	0	227	outbound_invoice	239			outbound_invoice_in		xml	invoice			f	1						0	f	text/plain	\N	2026-10-11 16:56:46.473583	f	f		0					0		0	2208	0	
240	3	1	0	0	225	outbound_invoice	translate									f	1						0	f	text/plain	\N	2026-10-11 16:56:47.209841	f	f		0					0		0	0	0	
249	3	330	248	259	240	outbound_invoice	249	5555555555555	1111111111111	outbound_invoice_in		edifact	INVOICD96AUNEAN008		invoice_xml2edifact	t	1		26			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:56:52.760117	f	f		0	edifact				0		0	744	0	
252	3	330	251	260	240	outbound_invoice	252	5555555555555	2222222222222	outbound_invoice_in		edifact	INVOICD96AUNEAN008		invoice_xml2edifact	t	1		27			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:56:54.096777	f	f		0	edifact				0		0	744	0	
255	3	330	254	261	240	outbound_invoice	255	6666666666666	1111111111111	outbound_invoice_in		edifact	INVOICD96AUNEAN008		invoice_xml2edifact	t	1		28			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:56:55.43703	f	f		0	edifact				0		0	744	0	
258	3	330	257	262	240	outbound_invoice	258	6666666666666	2222222222222	outbound_invoice_in		edifact	INVOICD96AUNEAN008		invoice_xml2edifact	t	1		29			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:56:56.370373	f	f		0	edifact				0		0	744	0	
246	3	330	245	263	240	outbound_invoice	246	SENDER	RECEIVER	outbound_invoice_in		edifact	INVOICD96AUNEAN008		invoice_xml2edifact	t	1		25			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:56:51.235213	f	f		0	edifact				0		0	744	0	
259	3	400	0	0	225	outbound_invoice	259	5555555555555	1111111111111	outbound_invoice_in		edifact	INVOICD96AUNEAN008			t	2		3			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:56:56.95735	f	f		0	edifact				0		0	2405	0	
260	3	400	0	0	225	outbound_invoice	260	5555555555555	2222222222222	outbound_invoice_in		edifact	INVOICD96AUNEAN008			t	1		4			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:56:57.497672	f	f		0	edifact				0		0	826	0	
261	3	400	0	0	225	outbound_invoice	261	6666666666666	1111111111111	outbound_invoice_in		edifact	INVOICD96AUNEAN008			t	1		3			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:56:57.788543	f	f		0	edifact				0		0	826	0	
262	3	400	0	0	225	outbound_invoice	262	6666666666666	2222222222222	outbound_invoice_in		edifact	INVOICD96AUNEAN008			t	1		4			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:56:58.05716	f	f		0	edifact				0		0	826	0	
263	3	400	0	0	225	outbound_invoice	263	SENDER	RECEIVER	outbound_invoice_in		edifact	INVOICD96AUNEAN008			t	1		2			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:56:58.481223	f	f		0	edifact				0		0	814	0	
271	3	520	264	0	270	outbound_invoice	/o/pg/bots/botssys/outfile/edifact_xml/edifact/invoic1.edi	5555555555555	1111111111111	outbound_invoice_in	outbound_invoice_out	edifact	INVOICD96AUNEAN008			t	2		3			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:57:00.683771	f	f		0	edifact				0		0	0	1	
264	3	500	259	0	225	outbound_invoice	259	5555555555555	1111111111111	outbound_invoice_in	outbound_invoice_out	edifact	INVOICD96AUNEAN008			t	2		3			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:56:58.887277	f	f		0	edifact				0		0	0	0	
272	3	520	265	0	270	outbound_invoice	/o/pg/bots/botssys/outfile/edifact_xml/edifact/invoic2.edi	5555555555555	2222222222222	outbound_invoice_in	outbound_invoice_out	edifact	INVOICD96AUNEAN008			t	1		4			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:57:01.770947	f	f		0	edifact				0		0	0	1	
265	3	500	260	0	225	outbound_invoice	260	5555555555555	2222222222222	outbound_invoice_in	outbound_invoice_out	edifact	INVOICD96AUNEAN008			t	1		4			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:56:59.034614	f	f		0	edifact				0		0	0	0	
273	3	520	266	0	270	outbound_invoice	/o/pg/bots/botssys/outfile/edifact_xml/edifact/invoic3.edi	6666666666666	1111111111111	outbound_invoice_in	outbound_invoice_out	edifact	INVOICD96AUNEAN008			t	1		3			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:57:02.038557	f	f		0	edifact				0		0	0	1	
266	3	500	261	0	225	outbound_invoice	261	6666666666666	1111111111111	outbound_invoice_in	outbound_invoice_out	edifact	INVOICD96AUNEAN008			t	1		3			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:56:59.26965	f	f		0	edifact				0		0	0	0	
274	3	520	267	0	270	outbound_invoice	/o/pg/bots/botssys/outfile/edifact_xml/edifact/invoic4.edi	6666666666666	2222222222222	outbound_invoice_in	outbound_invoice_out	edifact	INVOICD96AUNEAN008			t	1		4			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:57:02.591955	f	f		0	edifact				0		0	0	1	
267	3	500	262	0	225	outbound_invoice	262	6666666666666	2222222222222	outbound_invoice_in	outbound_invoice_out	edifact	INVOICD96AUNEAN008			t	1		4			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:56:59.508889	f	f		0	edifact				0		0	0	0	
275	3	520	268	0	270	outbound_invoice	/o/pg/bots/botssys/outfile/edifact_xml/edifact/invoic5.edi	SENDER	RECEIVER	outbound_invoice_in	outbound_invoice_out	edifact	INVOICD96AUNEAN008			t	1		2			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:57:03.147958	f	f		0	edifact				0		0	0	1	
268	3	500	263	0	225	outbound_invoice	263	SENDER	RECEIVER	outbound_invoice_in	outbound_invoice_out	edifact	INVOICD96AUNEAN008			t	1		2			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:56:59.700552	f	f		0	edifact				0		0	0	0	
270	3	1	0	0	269	outbound_invoice	outcommunicate									f	1						0	f	text/plain	\N	2026-10-11 16:57:00.459649	f	f		0					0		0	0	0	
269	3	1	0	0	225	outbound_invoice	run				outbound_invoice_out					f	1						0	f	text/plain	\N	2026-10-11 16:56:59.980772	f	f		0					0		0	0	0	
276	3	1	0	0	0		rundispatcher									f	1						0	f	text/plain	\N	2026-10-11 16:57:56.291759	f	f		0					0		0	0	0	
281	3	200	0	0	280	demo_partner_conversion	/o/pg/bots/botssys/infile/demo_work_with_partners/partner_conversion/frompartner1_topartner1_1.x12			demo_partner_conversion_in						f	1						0	f	text/plain	\N	2026-10-11 16:57:57.642968	f	f		0					0		0	0	0	
280	3	1	0	0	279	demo_partner_conversion	incommunicate									f	1						0	f	text/plain	\N	2026-10-11 16:57:57.5253	f	f		0					0		0	0	0	
279	3	1	0	0	278	demo_partner_conversion	run			demo_partner_conversion_in						f	1						0	f	text/plain	\N	2026-10-11 16:57:57.192978	f	f		0					0		0	0	0	
282	3	220	281	0	280	demo_partner_conversion	282			demo_partner_conversion_in		x12	x12			f	1						0	f	text/plain	\N	2026-10-11 16:57:57.700603	f	f		0					0		0	1229	0	
283	3	1	0	0	278	demo_partner_conversion	preprocess									f	1						0	f	text/plain	\N	2026-10-11 16:57:58.296383	f	f		0					0		0	0	0	
284	3	220	282	0	283	demo_partner_conversion	284			demo_partner_conversion_in		x12	x12			f	1						0	f	text/plain	\N	2026-10-11 16:57:58.334914	f	f		0					0		0	1227	0	
287	3	320	286	0	285	demo_partner_conversion	284	FROMPARTNER2	TOPARTNER2	demo_partner_conversion_in		x12	856004010		inn2out	t	1	P	0004			us-ascii	0	f	application/X12	\N	2026-10-11 16:58:07.296674	f	f		0	x12				0		0	0	0	
286	3	310	284	0	285	demo_partner_conversion	284	FROMPARTNER2	TOPARTNER2	demo_partner_conversion_in		x12	x12			t	1	P				us-ascii	0	f	application/X12	\N	2026-10-11 16:57:58.905306	f	f		0	x12				0		0	1227	0	
285	3	1	0	0	278	demo_partner_conversion	translate									f	1						0	f	text/plain	\N	2026-10-11 16:57:58.761238	f	f		0					0		0	0	0	
288	3	330	287	289	285	demo_partner_conversion	288	FROMPARTNER2	TOPARTNER2	demo_partner_conversion_in		x12	856004010		inn2out	t	1	P	30			us-ascii	0	f	application/X12	\N	2026-10-11 16:58:07.572906	f	f		0	x12				0		0	1037	0	
292	3	1	0	0	291	demo_partner_conversion	outcommunicate									f	1						0	f	text/plain	\N	2026-10-11 16:58:10.835116	f	f		0					0		0	0	0	
289	3	400	0	0	278	demo_partner_conversion	289	frompartner1	topartner1	demo_partner_conversion_in		x12	856004010			t	1	P	2			us-ascii	0	f	application/X12	\N	2026-10-11 16:58:08.964338	f	f		0	x12				0		0	1227	0	
278	3	1	0	0	277	demo_partner_conversion	routepart									f	1						0	f	text/plain	\N	2026-10-11 16:57:56.898821	f	f		0					0		0	0	0	
293	3	520	290	0	292	demo_partner_conversion	/o/pg/bots/botssys/outfile/demo_work_with_partners/partner_conversion/frompartner1_topartner1_2.x12	frompartner1	topartner1	demo_partner_conversion_in	demo_partner_conversion_out	x12	856004010			t	1	P	2			us-ascii	0	f	application/X12	\N	2026-10-11 16:58:10.900084	f	f		0	x12				0		0	0	1	
290	3	500	289	0	278	demo_partner_conversion	289	frompartner1	topartner1	demo_partner_conversion_in	demo_partner_conversion_out	x12	856004010			t	1	P	2			us-ascii	0	f	application/X12	\N	2026-10-11 16:58:10.371928	f	f		0	x12				0		0	0	0	
291	3	1	0	0	278	demo_partner_conversion	run				demo_partner_conversion_out					f	1						0	f	text/plain	\N	2026-10-11 16:58:10.495133	f	f		0					0		0	0	0	
277	3	1	0	0	276	demo_partner_conversion	router									f	1						0	f	text/plain	\N	2026-10-11 16:57:56.783572	f	f		0					0		0	0	0	
295	3	1	0	0	294	inbound_orders	routepart									f	1						0	f	text/plain	\N	2026-10-11 16:58:11.963101	f	f		0					0		0	0	0	
294	3	1	0	0	276	inbound_orders	router									f	1						0	f	text/plain	\N	2026-10-11 16:58:11.840111	f	f		0					0		0	0	0	
312	3	1	0	0	295	inbound_orders	translate									f	1						0	f	text/plain	\N	2026-10-11 16:58:15.898618	f	f		0					0		0	0	0	
298	3	200	0	0	297	inbound_orders	/o/pg/bots/botssys/infile/edifact_xml/edifact/0T0000000004.edi			inbound_orders_in						f	1						0	f	text/plain	\N	2026-10-11 16:58:12.475502	f	f		0					0		0	0	0	
305	3	220	304	0	297	inbound_orders	305			inbound_orders_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-11 16:58:14.237448	f	f		0					0		0	284	0	
300	3	200	0	0	297	inbound_orders	/o/pg/bots/botssys/infile/edifact_xml/edifact/0T0000000015.edi			inbound_orders_in						f	1						0	f	text/plain	\N	2026-10-11 16:58:13.106957	f	f		0					0		0	0	0	
306	3	1	0	0	295	inbound_orders	preprocess									f	1						0	f	text/plain	\N	2026-10-11 16:58:14.610837	f	f		0					0		0	0	0	
302	3	200	0	0	297	inbound_orders	/o/pg/bots/botssys/infile/edifact_xml/edifact/T0000000001.edi			inbound_orders_in						f	1						0	f	text/plain	\N	2026-10-11 16:58:13.575436	f	f		0					0		0	0	0	
304	3	200	0	0	297	inbound_orders	/o/pg/bots/botssys/infile/edifact_xml/edifact/T0000000002.edi			inbound_orders_in						f	1						0	f	text/plain	\N	2026-10-11 16:58:14.143977	f	f		0					0		0	0	0	
297	3	1	0	0	296	inbound_orders	incommunicate									f	1						0	f	text/plain	\N	2026-10-11 16:58:12.341354	f	f		0					0		0	0	0	
296	3	1	0	0	295	inbound_orders	run			inbound_orders_in						f	1						0	f	text/plain	\N	2026-10-11 16:58:12.200748	f	f		0					0		0	0	0	
520	3	310	506	0	513	outbound_invoice	506	5555555555555	1111111111111	outbound_invoice_in		xml	invoice			f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:59:36.677437	f	f		0					0		0	2208	0	
307	3	220	299	0	306	inbound_orders	307			inbound_orders_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-11 16:58:14.657165	f	f		0					0		0	489	0	
299	3	220	298	0	297	inbound_orders	299			inbound_orders_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-11 16:58:12.57262	f	f		0					0		0	779	0	
325	3	320	324	0	312	inbound_orders	310	PARTNER1	PARTNER2	inbound_orders_in		edifact	ORDERSD96AUNEAN008		orders_edifact2xml	t	1		T0000000001			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:58:20.26647	f	f		0	edifact				0		0	0	0	
301	3	220	300	0	297	inbound_orders	301			inbound_orders_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-11 16:58:13.199016	f	f		0					0		0	262	0	
303	3	220	302	0	297	inbound_orders	303			inbound_orders_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-11 16:58:13.698634	f	f		0					0		0	278	0	
317	3	330	316	0	312	inbound_orders	317	PARTNER1	PARTNER2	inbound_orders_in		xml	orders		orders_edifact2xml	f	1		T0000000004-2			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:18.762258	f	f		0					0		0	586	0	
314	3	320	313	0	312	inbound_orders	307	PARTNER1	PARTNER2	inbound_orders_in		edifact	ORDERSD96AUNEAN008		orders_edifact2xml	t	1		T0000000004-1			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:58:18.090749	f	f		0	edifact				0		0	0	0	
320	3	330	319	0	312	inbound_orders	320	PARTNER1	PARTNER2	inbound_orders_in		xml	orders		orders_edifact2xml	f	1		T0000000004-3			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:19.204404	f	f		0					0		0	586	0	
316	3	320	313	0	312	inbound_orders	307	PARTNER1	PARTNER2	inbound_orders_in		edifact	ORDERSD96AUNEAN008		orders_edifact2xml	t	1		T0000000004-2			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:58:18.60432	f	f		0	edifact				0		0	0	0	
313	3	310	307	0	312	inbound_orders	307	PARTNER1	PARTNER2	inbound_orders_in		edifact	edifact			t	1					UNOA	0	f	application/EDIFACT	\N	2026-10-11 16:58:15.94169	f	f		0	edifact				0		0	489	0	
309	3	220	301	0	306	inbound_orders	309			inbound_orders_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-11 16:58:15.014618	f	f		0					0		0	261	0	
323	3	330	322	0	312	inbound_orders	323	PARTNER1	PARTNER2	inbound_orders_in		xml	orders		orders_edifact2xml	f	1		T0000000015			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:19.788611	f	f		0					0		0	584	0	
319	3	320	318	0	312	inbound_orders	308	PARTNER1	PARTNER2	inbound_orders_in		edifact	ORDERSD96AUNEAN008		orders_edifact2xml	t	1		T0000000004-3			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:58:19.131716	f	f		0	edifact				0		0	0	0	
318	3	310	308	0	312	inbound_orders	308	PARTNER1	PARTNER2	inbound_orders_in		edifact	edifact			t	1					UNOA	0	f	application/EDIFACT	\N	2026-10-11 16:58:19.09529	f	f		0	edifact				0		0	286	0	
308	3	220	299	0	306	inbound_orders	308			inbound_orders_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-11 16:58:14.758519	f	f		0					0		0	286	0	
326	3	330	325	0	312	inbound_orders	326	PARTNER1	PARTNER2	inbound_orders_in		xml	orders		orders_edifact2xml	f	1		T0000000001			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:20.279372	f	f		0					0		0	584	0	
322	3	320	321	0	312	inbound_orders	309	PARTNER1	PARTNER2	inbound_orders_in		edifact	ORDERSD96AUNEAN008		orders_edifact2xml	t	1		T0000000015			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:58:19.656306	f	f		0	edifact				0		0	0	0	
321	3	310	309	0	312	inbound_orders	309	PARTNER1	PARTNER2	inbound_orders_in		edifact	edifact			t	1					UNOA	0	f	application/EDIFACT	\N	2026-10-11 16:58:19.594058	f	f		0	edifact				0		0	261	0	
329	3	330	328	0	312	inbound_orders	329	PARTNER1	PARTNER2	inbound_orders_in		xml	orders		orders_edifact2xml	f	1		T0000000002-1			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:21.047615	f	f		0					0		0	586	0	
324	3	310	310	0	312	inbound_orders	310	PARTNER1	PARTNER2	inbound_orders_in		edifact	edifact			t	1					UNOA	0	f	application/EDIFACT	\N	2026-10-11 16:58:20.202662	f	f		0	edifact				0		0	276	0	
310	3	220	303	0	306	inbound_orders	310			inbound_orders_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-11 16:58:15.370787	f	f		0					0		0	276	0	
328	3	320	327	0	312	inbound_orders	311	PARTNER1	PARTNER2	inbound_orders_in		edifact	ORDERSD96AUNEAN008		orders_edifact2xml	t	1		T0000000002-1			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:58:20.843004	f	f		0	edifact				0		0	0	0	
327	3	310	311	0	312	inbound_orders	311	PARTNER1	PARTNER2	inbound_orders_in		edifact	edifact			t	1					UNOA	0	f	application/EDIFACT	\N	2026-10-11 16:58:20.765552	f	f		0	edifact				0		0	282	0	
311	3	220	305	0	306	inbound_orders	311			inbound_orders_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-11 16:58:15.57747	f	f		0					0		0	282	0	
315	3	330	314	0	312	inbound_orders	315	PARTNER1	PARTNER2	inbound_orders_in		xml	orders		orders_edifact2xml	f	1		T0000000004-1			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:18.209222	f	f		0					0		0	586	0	
344	3	520	336	0	343	inbound_orders	/o/pg/bots/botssys/outfile/edifact_xml/xml/orders_7.xml	PARTNER1	PARTNER2	inbound_orders_in	inbound_orders_out	xml	orders			f	1		T0000000004-1			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:24.64251	f	f		0					0		0	0	1	
336	3	500	330	0	295	inbound_orders	315	PARTNER1	PARTNER2	inbound_orders_in	inbound_orders_out	xml	orders			f	1		T0000000004-1			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:23.283691	f	f		0					0		0	0	0	
345	3	520	337	0	343	inbound_orders	/o/pg/bots/botssys/outfile/edifact_xml/xml/orders_8.xml	PARTNER1	PARTNER2	inbound_orders_in	inbound_orders_out	xml	orders			f	1		T0000000004-2			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:24.987618	f	f		0					0		0	0	1	
337	3	500	331	0	295	inbound_orders	317	PARTNER1	PARTNER2	inbound_orders_in	inbound_orders_out	xml	orders			f	1		T0000000004-2			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:23.41036	f	f		0					0		0	0	0	
349	3	520	341	0	343	inbound_orders	/o/pg/bots/botssys/outfile/edifact_xml/xml/orders_12.xml	PARTNER1	PARTNER2	inbound_orders_in	inbound_orders_out	xml	orders			f	1		T0000000002-1			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:26.019808	f	f		0					0		0	0	1	
330	3	400	315	0	295	inbound_orders	315	PARTNER1	PARTNER2	inbound_orders_in		xml	orders			f	1		T0000000004-1			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:21.689481	f	f		0					0		0	586	0	
341	3	500	335	0	295	inbound_orders	329	PARTNER1	PARTNER2	inbound_orders_in	inbound_orders_out	xml	orders			f	1		T0000000002-1			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:24.282692	f	f		0					0		0	0	0	
331	3	400	317	0	295	inbound_orders	317	PARTNER1	PARTNER2	inbound_orders_in		xml	orders			f	1		T0000000004-2			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:21.930235	f	f		0					0		0	586	0	
343	3	1	0	0	342	inbound_orders	outcommunicate									f	1						0	f	text/plain	\N	2026-10-11 16:58:24.585004	f	f		0					0		0	0	0	
332	3	400	320	0	295	inbound_orders	320	PARTNER1	PARTNER2	inbound_orders_in		xml	orders			f	1		T0000000004-3			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:22.262102	f	f		0					0		0	586	0	
342	3	1	0	0	295	inbound_orders	run				inbound_orders_out					f	1						0	f	text/plain	\N	2026-10-11 16:58:24.511665	f	f		0					0		0	0	0	
333	3	400	323	0	295	inbound_orders	323	PARTNER1	PARTNER2	inbound_orders_in		xml	orders			f	1		T0000000015			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:22.888068	f	f		0					0		0	584	0	
334	3	400	326	0	295	inbound_orders	326	PARTNER1	PARTNER2	inbound_orders_in		xml	orders			f	1		T0000000001			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:23.042007	f	f		0					0		0	584	0	
354	3	200	0	0	353	myfirstroute	/o/pg/bots/botssys/infile/my_first_plugin/order01.edi			myfirstroute_in						f	1						0	f	text/plain	\N	2026-10-11 16:58:27.089776	f	f		0					0		0	0	0	
335	3	400	329	0	295	inbound_orders	329	PARTNER1	PARTNER2	inbound_orders_in		xml	orders			f	1		T0000000002-1			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:23.19097	f	f		0					0		0	586	0	
346	3	520	338	0	343	inbound_orders	/o/pg/bots/botssys/outfile/edifact_xml/xml/orders_9.xml	PARTNER1	PARTNER2	inbound_orders_in	inbound_orders_out	xml	orders			f	1		T0000000004-3			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:25.299902	f	f		0					0		0	0	1	
338	3	500	332	0	295	inbound_orders	320	PARTNER1	PARTNER2	inbound_orders_in	inbound_orders_out	xml	orders			f	1		T0000000004-3			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:23.509645	f	f		0					0		0	0	0	
347	3	520	339	0	343	inbound_orders	/o/pg/bots/botssys/outfile/edifact_xml/xml/orders_10.xml	PARTNER1	PARTNER2	inbound_orders_in	inbound_orders_out	xml	orders			f	1		T0000000015			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:25.550231	f	f		0					0		0	0	1	
339	3	500	333	0	295	inbound_orders	323	PARTNER1	PARTNER2	inbound_orders_in	inbound_orders_out	xml	orders			f	1		T0000000015			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:23.648681	f	f		0					0		0	0	0	
348	3	520	340	0	343	inbound_orders	/o/pg/bots/botssys/outfile/edifact_xml/xml/orders_11.xml	PARTNER1	PARTNER2	inbound_orders_in	inbound_orders_out	xml	orders			f	1		T0000000001			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:25.793438	f	f		0					0		0	0	1	
340	3	500	334	0	295	inbound_orders	326	PARTNER1	PARTNER2	inbound_orders_in	inbound_orders_out	xml	orders			f	1		T0000000001			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:23.987571	f	f		0					0		0	0	0	
362	3	220	355	0	360	myfirstroute	362			myfirstroute_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-11 16:58:28.901492	f	f		0					0		0	416	0	
356	3	200	0	0	353	myfirstroute	/o/pg/bots/botssys/infile/my_first_plugin/order02.edi			myfirstroute_in						f	1						0	f	text/plain	\N	2026-10-11 16:58:27.77593	f	f		0					0		0	0	0	
358	3	200	0	0	353	myfirstroute	/o/pg/bots/botssys/infile/my_first_plugin/order03.edi			myfirstroute_in						f	1						0	f	text/plain	\N	2026-10-11 16:58:28.237818	f	f		0					0		0	0	0	
353	3	1	0	0	352	myfirstroute	incommunicate									f	1						0	f	text/plain	\N	2026-10-11 16:58:26.940802	f	f		0					0		0	0	0	
352	3	1	0	0	351	myfirstroute	run			myfirstroute_in						f	1						0	f	text/plain	\N	2026-10-11 16:58:26.751155	f	f		0					0		0	0	0	
360	3	1	0	0	351	myfirstroute	preprocess									f	1						0	f	text/plain	\N	2026-10-11 16:58:28.720277	f	f		0					0		0	0	0	
363	3	220	357	0	360	myfirstroute	363			myfirstroute_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-11 16:58:29.312478	f	f		0					0		0	269	0	
355	3	220	354	0	353	myfirstroute	355			myfirstroute_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-11 16:58:27.208221	f	f		0					0		0	920	0	
351	3	1	0	0	350	myfirstroute	routepart									f	1						0	f	text/plain	\N	2026-10-11 16:58:26.57743	f	f		0					0		0	0	0	
357	3	220	356	0	353	myfirstroute	357			myfirstroute_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-11 16:58:27.884207	f	f		0					0		0	270	0	
359	3	220	358	0	353	myfirstroute	359			myfirstroute_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-11 16:58:28.283559	f	f		0					0		0	267	0	
361	3	220	355	0	360	myfirstroute	361			myfirstroute_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-11 16:58:28.772046	f	f		0					0		0	500	0	
350	3	1	0	0	276	myfirstroute	router									f	1						0	f	text/plain	\N	2026-10-11 16:58:26.535714	f	f		0					0		0	0	0	
374	3	310	363	0	365	myfirstroute	363	8712345678906	PARTNER2	myfirstroute_in		edifact	edifact			t	1					UNOA	0	f	application/EDIFACT	\N	2026-10-11 16:58:33.274422	f	f		0	edifact				0		0	269	0	
367	3	320	366	0	365	myfirstroute	361	8712345678906	PARTNER2	myfirstroute_in		edifact	ORDERSD96AUNEAN008		orders_edifact2xml	t	1		T0000000004-1			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:58:30.571064	f	f		0	edifact				0		0	0	0	
682	3	1	0	0	671	outbound_asn	translate									f	1						0	f	text/plain	\N	2026-10-12 03:50:53.105471	f	f		0					0		0	0	0	
369	3	320	366	0	365	myfirstroute	361	8712345678906	PARTNER2	myfirstroute_in		edifact	ORDERSD96AUNEAN008		orders_edifact2xml	t	1		T0000000004-2			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:58:31.450841	f	f		0	edifact				0		0	0	0	
366	3	310	361	0	365	myfirstroute	361	8712345678906	PARTNER2	myfirstroute_in		edifact	edifact			t	1					UNOA	0	f	application/EDIFACT	\N	2026-10-11 16:58:30.504517	f	f		0	edifact				0		0	500	0	
372	3	320	371	0	365	myfirstroute	362	8712345678906	PARTNER2	myfirstroute_in		edifact	ORDERSD96AUNEAN008		orders_edifact2xml	t	1		T0000000004-3			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:58:32.534847	f	f		0	edifact				0		0	0	0	
371	3	310	362	0	365	myfirstroute	362	8712345678906	PARTNER2	myfirstroute_in		edifact	edifact			t	1					UNOA	0	f	application/EDIFACT	\N	2026-10-11 16:58:32.440017	f	f		0	edifact				0		0	416	0	
375	3	320	374	0	365	myfirstroute	363	8712345678906	PARTNER2	myfirstroute_in		edifact	ORDERSD96AUNEAN008		orders_edifact2xml	t	1		T0000000015			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:58:33.328071	f	f		0	edifact				0		0	0	0	
378	3	320	377	0	365	myfirstroute	364	8712345678906	PARTNER2	myfirstroute_in		edifact	ORDERSD96AUNEAN008		orders_edifact2xml	t	1		T0000000001			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:58:34.293871	f	f		0	edifact				0		0	0	0	
377	3	310	364	0	365	myfirstroute	364	8712345678906	PARTNER2	myfirstroute_in		edifact	edifact			t	1					UNOA	0	f	application/EDIFACT	\N	2026-10-11 16:58:34.265891	f	f		0	edifact				0		0	265	0	
364	3	220	359	0	360	myfirstroute	364			myfirstroute_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-11 16:58:30.014457	f	f		0					0		0	265	0	
365	3	1	0	0	351	myfirstroute	translate									f	1						0	f	text/plain	\N	2026-10-11 16:58:30.446635	f	f		0					0		0	0	0	
368	3	330	367	0	365	myfirstroute	368	8712345678906	PARTNER2	myfirstroute_in		xml	orders		orders_edifact2xml	f	1		ORDT0000000004-1			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:30.866274	f	f		0					0		0	594	0	
391	3	1	0	0	390	myfirstroute	outcommunicate									f	1						0	f	text/plain	\N	2026-10-11 16:58:37.811729	f	f		0					0		0	0	0	
370	3	330	369	0	365	myfirstroute	370	8712345678906	PARTNER2	myfirstroute_in		xml	orders		orders_edifact2xml	f	1		ORDT0000000004-2			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:31.804933	f	f		0					0		0	594	0	
373	3	330	372	0	365	myfirstroute	373	8712345678906	PARTNER2	myfirstroute_in		xml	orders		orders_edifact2xml	f	1		ORDT0000000004-3			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:32.703136	f	f		0					0		0	1006	0	
384	3	400	379	0	351	myfirstroute	379	8712345678906	PARTNER2	myfirstroute_in		xml	orders			f	1		ORDT0000000001			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:35.952871	f	f		0					0		0	592	0	
376	3	330	375	0	365	myfirstroute	376	8712345678906	PARTNER2	myfirstroute_in		xml	orders		orders_edifact2xml	f	1		ORDT0000000015			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:33.686691	f	f		0					0		0	592	0	
379	3	330	378	0	365	myfirstroute	379	8712345678906	PARTNER2	myfirstroute_in		xml	orders		orders_edifact2xml	f	1		ORDT0000000001			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:34.381482	f	f		0					0		0	592	0	
380	3	400	368	0	351	myfirstroute	368	8712345678906	PARTNER2	myfirstroute_in		xml	orders			f	1		ORDT0000000004-1			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:34.960879	f	f		0					0		0	594	0	
381	3	400	370	0	351	myfirstroute	370	8712345678906	PARTNER2	myfirstroute_in		xml	orders			f	1		ORDT0000000004-2			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:35.219502	f	f		0					0		0	594	0	
382	3	400	373	0	351	myfirstroute	373	8712345678906	PARTNER2	myfirstroute_in		xml	orders			f	1		ORDT0000000004-3			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:35.405458	f	f		0					0		0	1006	0	
389	3	500	384	0	351	myfirstroute	379	8712345678906	PARTNER2	myfirstroute_in	myfirstroute_out	xml	orders			f	1		ORDT0000000001			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:37.595508	f	f		0					0		0	0	0	
383	3	400	376	0	351	myfirstroute	376	8712345678906	PARTNER2	myfirstroute_in		xml	orders			f	1		ORDT0000000015			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:35.617945	f	f		0					0		0	592	0	
392	3	520	385	0	391	myfirstroute	/o/pg/bots/botssys/outfile/my_first_plugin/orders6.inh	8712345678906	PARTNER2	myfirstroute_in	myfirstroute_out	xml	orders			f	1		ORDT0000000004-1			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:37.870861	f	f		0					0		0	0	1	
385	3	500	380	0	351	myfirstroute	368	8712345678906	PARTNER2	myfirstroute_in	myfirstroute_out	xml	orders			f	1		ORDT0000000004-1			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:36.193109	f	f		0					0		0	0	0	
393	3	520	386	0	391	myfirstroute	/o/pg/bots/botssys/outfile/my_first_plugin/orders7.inh	8712345678906	PARTNER2	myfirstroute_in	myfirstroute_out	xml	orders			f	1		ORDT0000000004-2			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:38.151197	f	f		0					0		0	0	1	
386	3	500	381	0	351	myfirstroute	370	8712345678906	PARTNER2	myfirstroute_in	myfirstroute_out	xml	orders			f	1		ORDT0000000004-2			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:36.426401	f	f		0					0		0	0	0	
394	3	520	387	0	391	myfirstroute	/o/pg/bots/botssys/outfile/my_first_plugin/orders8.inh	8712345678906	PARTNER2	myfirstroute_in	myfirstroute_out	xml	orders			f	1		ORDT0000000004-3			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:38.495746	f	f		0					0		0	0	1	
387	3	500	382	0	351	myfirstroute	373	8712345678906	PARTNER2	myfirstroute_in	myfirstroute_out	xml	orders			f	1		ORDT0000000004-3			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:36.798422	f	f		0					0		0	0	0	
388	3	500	383	0	351	myfirstroute	376	8712345678906	PARTNER2	myfirstroute_in	myfirstroute_out	xml	orders			f	1		ORDT0000000015			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:37.312504	f	f		0					0		0	0	0	
390	3	1	0	0	351	myfirstroute	run				myfirstroute_out					f	1						0	f	text/plain	\N	2026-10-11 16:58:37.696877	f	f		0					0		0	0	0	
395	3	520	388	0	391	myfirstroute	/o/pg/bots/botssys/outfile/my_first_plugin/orders9.inh	8712345678906	PARTNER2	myfirstroute_in	myfirstroute_out	xml	orders			f	1		ORDT0000000015			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:39.072236	f	f		0					0		0	0	1	
396	3	520	389	0	391	myfirstroute	/o/pg/bots/botssys/outfile/my_first_plugin/orders10.inh	8712345678906	PARTNER2	myfirstroute_in	myfirstroute_out	xml	orders			f	1		ORDT0000000001			utf-8	0	f	text/xml 	\N	2026-10-11 16:58:39.374406	f	f		0					0		0	0	1	
401	3	200	0	0	400	outbound_asn	/o/pg/bots/botssys/infile/demo_work_with_partners/asn/856_PARTNER1_03.xml			outbound_asn_in						f	1						0	f	text/plain	\N	2026-10-11 16:58:40.750297	f	f		0					0		0	0	0	
411	3	320	410	0	409	outbound_asn	402	SENDER	PARTNER1	outbound_asn_in		xml	asn		asn_xml2x12_default	f	1	P				utf-8	0	f	text/xml 	\N	2026-10-11 16:58:43.992602	f	f		0					0		0	0	0	
403	3	200	0	0	400	outbound_asn	/o/pg/bots/botssys/infile/demo_work_with_partners/asn/856_PARTNER2_01.xml			outbound_asn_in						f	1						0	f	text/plain	\N	2026-10-11 16:58:41.053344	f	f		0					0		0	0	0	
410	3	310	402	0	409	outbound_asn	402	SENDER	PARTNER1	outbound_asn_in		xml	asn			f	1	P				utf-8	0	f	text/xml 	\N	2026-10-11 16:58:43.372813	f	f		0					0		0	16468	0	
405	3	200	0	0	400	outbound_asn	/o/pg/bots/botssys/infile/demo_work_with_partners/asn/856_PARTNER2_04.xml			outbound_asn_in						f	1						0	f	text/plain	\N	2026-10-11 16:58:41.439013	f	f		0					0		0	0	0	
402	3	220	401	0	400	outbound_asn	402			outbound_asn_in		xml	asn			f	1						0	f	text/plain	\N	2026-10-11 16:58:40.821418	f	f		0					0		0	16468	0	
407	3	200	0	0	400	outbound_asn	/o/pg/bots/botssys/infile/demo_work_with_partners/asn/856_PARTNER3_02.xml			outbound_asn_in						f	1						0	f	text/plain	\N	2026-10-11 16:58:41.773042	f	f		0					0		0	0	0	
400	3	1	0	0	399	outbound_asn	incommunicate									f	1						0	f	text/plain	\N	2026-10-11 16:58:40.650071	f	f		0					0		0	0	0	
399	3	1	0	0	398	outbound_asn	run			outbound_asn_in						f	1						0	f	text/plain	\N	2026-10-11 16:58:40.540798	f	f		0					0		0	0	0	
420	3	320	419	0	409	outbound_asn	408	SENDER	PARTNER3	outbound_asn_in		xml	asn		asn_xml2x12_noSSCC	f	1	P				utf-8	0	f	text/xml 	\N	2026-10-11 16:58:48.401383	f	f		0					0		0	0	0	
419	3	310	408	0	409	outbound_asn	408	SENDER	PARTNER3	outbound_asn_in		xml	asn			f	1	P				utf-8	0	f	text/xml 	\N	2026-10-11 16:58:48.370176	f	f		0					0		0	3396	0	
417	3	320	416	0	409	outbound_asn	406	SENDER	PARTNER2	outbound_asn_in		xml	asn		asn_xml2x12_partner2	f	1	P				utf-8	0	f	text/xml 	\N	2026-10-11 16:58:47.350631	f	f		0					0		0	0	0	
416	3	310	406	0	409	outbound_asn	406	SENDER	PARTNER2	outbound_asn_in		xml	asn			f	1	P				utf-8	0	f	text/xml 	\N	2026-10-11 16:58:47.223625	f	f		0					0		0	1192	0	
406	3	220	405	0	400	outbound_asn	406			outbound_asn_in		xml	asn			f	1						0	f	text/plain	\N	2026-10-11 16:58:41.484017	f	f		0					0		0	1192	0	
414	3	320	413	0	409	outbound_asn	404	SENDER	PARTNER2	outbound_asn_in		xml	asn		asn_xml2x12_partner2	f	1	P				utf-8	0	f	text/xml 	\N	2026-10-11 16:58:46.15678	f	f		0					0		0	0	0	
413	3	310	404	0	409	outbound_asn	404	SENDER	PARTNER2	outbound_asn_in		xml	asn			f	1	P				utf-8	0	f	text/xml 	\N	2026-10-11 16:58:46.072151	f	f		0					0		0	4523	0	
404	3	220	403	0	400	outbound_asn	404			outbound_asn_in		xml	asn			f	1						0	f	text/plain	\N	2026-10-11 16:58:41.210369	f	f		0					0		0	4523	0	
408	3	220	407	0	400	outbound_asn	408			outbound_asn_in		xml	asn			f	1						0	f	text/plain	\N	2026-10-11 16:58:41.912054	f	f		0					0		0	3396	0	
409	3	1	0	0	398	outbound_asn	translate									f	1						0	f	text/plain	\N	2026-10-11 16:58:42.50939	f	f		0					0		0	0	0	
412	3	330	411	422	409	outbound_asn	412	SENDER	PARTNER1	outbound_asn_in		x12	856004010		asn_xml2x12_default	t	1	P	42			us-ascii	0	f	application/X12	\N	2026-10-11 16:58:44.110471	f	f		0	x12				0		0	4056	0	
415	3	330	414	423	409	outbound_asn	415	SENDER	PARTNER2	outbound_asn_in		x12	856004010		asn_xml2x12_partner2	t	1	P	43			us-ascii	0	f	application/X12	\N	2026-10-11 16:58:46.379704	f	f		0	x12				0		0	1603	0	
418	3	330	417	423	409	outbound_asn	418	SENDER	PARTNER2	outbound_asn_in		x12	856004010		asn_xml2x12_partner2	t	1	P	44			us-ascii	0	f	application/X12	\N	2026-10-11 16:58:47.615631	f	f		0	x12				0		0	430	0	
421	3	330	420	424	409	outbound_asn	421	SENDER	PARTNER3	outbound_asn_in		x12	856004010		asn_xml2x12_noSSCC	t	1	P	45			us-ascii	0	f	application/X12	\N	2026-10-11 16:58:48.63949	f	f		0	x12				0		0	1037	0	
398	3	1	0	0	397	outbound_asn	routepart									f	1						0	f	text/plain	\N	2026-10-11 16:58:40.413133	f	f		0					0		0	0	0	
428	3	1	0	0	427	outbound_asn	outcommunicate									f	1						0	f	text/plain	\N	2026-10-11 16:58:54.174234	f	f		0					0		0	0	0	
424	3	400	0	0	398	outbound_asn	424	SENDER	PARTNER3	outbound_asn_in		x12	856004010			t	1	P	6			us-ascii	0	f	application/X12	\N	2026-10-11 16:58:52.556313	f	f		0	x12				0		0	1219	0	
425	3	1	0	0	397	outbound_asn	routepart									f	1						0	f	text/plain	\N	2026-10-11 16:58:53.400248	f	f		0					0		0	0	0	
429	3	520	426	0	428	outbound_asn	/o/pg/bots/botssys/outfile/demo_work_with_partners/outbound_856/PARTNER3_pgroupA_20261011_2.x12	SENDER	PARTNER3	outbound_asn_in	outbound_asn_out_pgroupA	x12	856004010			t	1	P	6			us-ascii	0	f	application/X12	\N	2026-10-11 16:58:54.292638	f	f		0	x12				0		0	0	1	
426	3	500	424	0	425	outbound_asn	424	SENDER	PARTNER3	outbound_asn_in	outbound_asn_out_pgroupA	x12	856004010			t	1	P	6			us-ascii	0	f	application/X12	\N	2026-10-11 16:58:53.537515	f	f		0	x12				0		0	0	0	
427	3	1	0	0	425	outbound_asn	run				outbound_asn_out_pgroupA					f	1						0	f	text/plain	\N	2026-10-11 16:58:53.991422	f	f		0					0		0	0	0	
423	3	400	0	0	398	outbound_asn	423	SENDER	PARTNER2	outbound_asn_in		x12	856004010			t	2	P	5			us-ascii	0	f	application/X12	\N	2026-10-11 16:58:51.532924	f	f		0	x12				0		0	2215	0	
422	3	400	0	0	398	outbound_asn	422	SENDER	PARTNER1	outbound_asn_in		x12	856004010			t	1	P	4			us-ascii	0	f	application/X12	\N	2026-10-11 16:58:49.693615	f	f		0	x12				0		0	4238	0	
397	3	1	0	0	276	outbound_asn	router									f	1						0	f	text/plain	\N	2026-10-11 16:58:40.315869	f	f		0					0		0	0	0	
446	3	200	0	0	443	outbound_desadv	/o/pg/bots/botssys/infile/edifact_xml/xml/desadvfull01.xml			outbound_desadv_in						f	1						0	f	text/plain	\N	2026-10-11 16:59:00.978926	f	f		0					0		0	0	0	
434	3	520	431	0	433	outbound_asn	/o/pg/bots/botssys/outfile/demo_work_with_partners/outbound_856/PARTNER2_20261011_2.x12	SENDER	PARTNER2	outbound_asn_in	outbound_asn_out_partner2	x12	856004010			t	2	P	5			us-ascii	0	f	application/X12	\N	2026-10-11 16:58:56.050756	f	f		0	x12				0		0	0	1	
431	3	500	423	0	430	outbound_asn	423	SENDER	PARTNER2	outbound_asn_in	outbound_asn_out_partner2	x12	856004010			t	2	P	5			us-ascii	0	f	application/X12	\N	2026-10-11 16:58:55.385587	f	f		0	x12				0		0	0	0	
433	3	1	0	0	432	outbound_asn	outcommunicate									f	1						0	f	text/plain	\N	2026-10-11 16:58:55.936367	f	f		0					0		0	0	0	
432	3	1	0	0	430	outbound_asn	run				outbound_asn_out_partner2					f	1						0	f	text/plain	\N	2026-10-11 16:58:55.702292	f	f		0					0		0	0	0	
430	3	1	0	0	397	outbound_asn	routepart									f	1						0	f	text/plain	\N	2026-10-11 16:58:55.273229	f	f		0					0		0	0	0	
445	3	220	444	0	443	outbound_desadv	445			outbound_desadv_in		xml	desadv			f	1						0	f	text/plain	\N	2026-10-11 16:59:00.075108	f	f		0					0		0	1320	0	
439	3	520	436	0	438	outbound_asn	/o/pg/bots/botssys/outfile/demo_work_with_partners/outbound_856/PARTNER1_20261011_2.x12	SENDER	PARTNER1	outbound_asn_in	outbound_asn_out	x12	856004010			t	1	P	4			us-ascii	0	f	application/X12	\N	2026-10-11 16:58:57.324407	f	f		0	x12				0		0	0	1	
436	3	500	422	0	435	outbound_asn	422	SENDER	PARTNER1	outbound_asn_in	outbound_asn_out	x12	856004010			t	1	P	4			us-ascii	0	f	application/X12	\N	2026-10-11 16:58:56.680341	f	f		0	x12				0		0	0	0	
438	3	1	0	0	437	outbound_asn	outcommunicate									f	1						0	f	text/plain	\N	2026-10-11 16:58:57.251203	f	f		0					0		0	0	0	
437	3	1	0	0	435	outbound_asn	run				outbound_asn_out					f	1						0	f	text/plain	\N	2026-10-11 16:58:56.968197	f	f		0					0		0	0	0	
435	3	1	0	0	397	outbound_asn	routepart									f	1						0	f	text/plain	\N	2026-10-11 16:58:56.62949	f	f		0					0		0	0	0	
447	3	220	446	0	443	outbound_desadv	447			outbound_desadv_in		xml	desadv			f	1						0	f	text/plain	\N	2026-10-11 16:59:01.337979	f	f		0					0		0	11810	0	
449	3	220	448	0	443	outbound_desadv	449			outbound_desadv_in		xml	desadv			f	1						0	f	text/plain	\N	2026-10-11 16:59:02.203203	f	f		0					0		0	1571	0	
444	3	200	0	0	443	outbound_desadv	/o/pg/bots/botssys/infile/edifact_xml/xml/desadv1923.xml			outbound_desadv_in						f	1						0	f	text/plain	\N	2026-10-11 16:58:59.904938	f	f		0					0		0	0	0	
451	3	220	450	0	443	outbound_desadv	451			outbound_desadv_in		xml	desadv			f	1						0	f	text/plain	\N	2026-10-11 16:59:02.774978	f	f		0					0		0	1503	0	
448	3	200	0	0	443	outbound_desadv	/o/pg/bots/botssys/infile/edifact_xml/xml/desadvtest01.xml			outbound_desadv_in						f	1						0	f	text/plain	\N	2026-10-11 16:59:02.054075	f	f		0					0		0	0	0	
453	3	220	452	0	443	outbound_desadv	453			outbound_desadv_in		xml	desadv			f	1						0	f	text/plain	\N	2026-10-11 16:59:03.561612	f	f		0					0		0	1503	0	
450	3	200	0	0	443	outbound_desadv	/o/pg/bots/botssys/infile/edifact_xml/xml/desadvtest5-1.xml			outbound_desadv_in						f	1						0	f	text/plain	\N	2026-10-11 16:59:02.57327	f	f		0					0		0	0	0	
441	3	1	0	0	440	outbound_desadv	routepart									f	1						0	f	text/plain	\N	2026-10-11 16:58:59.082123	f	f		0					0		0	0	0	
452	3	200	0	0	443	outbound_desadv	/o/pg/bots/botssys/infile/edifact_xml/xml/desadvtest5-2.xml			outbound_desadv_in						f	1						0	f	text/plain	\N	2026-10-11 16:59:03.409397	f	f		0					0		0	0	0	
440	3	1	0	0	276	outbound_desadv	router									f	1						0	f	text/plain	\N	2026-10-11 16:58:58.846598	f	f		0					0		0	0	0	
454	3	200	0	0	443	outbound_desadv	/o/pg/bots/botssys/infile/edifact_xml/xml/desadvtest6-1.xml			outbound_desadv_in						f	1						0	f	text/plain	\N	2026-10-11 16:59:04.004468	f	f		0					0		0	0	0	
456	3	200	0	0	443	outbound_desadv	/o/pg/bots/botssys/infile/edifact_xml/xml/desadvtest6-2.xml			outbound_desadv_in						f	1						0	f	text/plain	\N	2026-10-11 16:59:04.466915	f	f		0					0		0	0	0	
443	3	1	0	0	442	outbound_desadv	incommunicate									f	1						0	f	text/plain	\N	2026-10-11 16:58:59.450802	f	f		0					0		0	0	0	
442	3	1	0	0	441	outbound_desadv	run			outbound_desadv_in						f	1						0	f	text/plain	\N	2026-10-11 16:58:59.185276	f	f		0					0		0	0	0	
524	3	320	523	0	513	outbound_invoice	508	5555555555555	2222222222222	outbound_invoice_in		xml	invoice		invoice_xml2edifact	f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:59:38.37452	f	f		0					0		0	0	0	
523	3	310	508	0	513	outbound_invoice	508	5555555555555	2222222222222	outbound_invoice_in		xml	invoice			f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:59:38.270256	f	f		0					0		0	2208	0	
526	3	310	510	0	513	outbound_invoice	510	6666666666666	1111111111111	outbound_invoice_in		xml	invoice			f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:59:39.711243	f	f		0					0		0	2208	0	
527	3	320	526	0	513	outbound_invoice	510	6666666666666	1111111111111	outbound_invoice_in		xml	invoice		invoice_xml2edifact	f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:59:39.809342	f	f		0					0		0	0	0	
529	3	310	512	0	513	outbound_invoice	512	6666666666666	2222222222222	outbound_invoice_in		xml	invoice			f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:59:40.357057	f	f		0					0		0	2208	0	
530	3	320	529	0	513	outbound_invoice	512	6666666666666	2222222222222	outbound_invoice_in		xml	invoice		invoice_xml2edifact	f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:59:40.443516	f	f		0					0		0	0	0	
528	3	330	527	534	513	outbound_invoice	528	6666666666666	1111111111111	outbound_invoice_in		edifact	INVOICD96AUNEAN008		invoice_xml2edifact	t	1		57			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:39.912411	f	f		0	edifact				0		0	744	0	
533	3	400	0	0	498	outbound_invoice	533	5555555555555	2222222222222	outbound_invoice_in		edifact	INVOICD96AUNEAN008			t	1		8			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:42.425565	f	f		0	edifact				0		0	826	0	
468	3	310	451	0	458	outbound_desadv	451	5555555555555	1111111111111	outbound_desadv_in		xml	desadv			f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:59:11.697778	f	f		0					0		0	1503	0	
460	3	320	459	0	458	outbound_desadv	445	5555555555555	1111111111111	outbound_desadv_in		xml	desadv		desadv_xml2edifact	f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:59:07.294506	f	f		0					0		0	0	0	
459	3	310	445	0	458	outbound_desadv	445	5555555555555	1111111111111	outbound_desadv_in		xml	desadv			f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:59:06.034954	f	f		0					0		0	1320	0	
455	3	220	454	0	443	outbound_desadv	455			outbound_desadv_in		xml	desadv			f	1						0	f	text/plain	\N	2026-10-11 16:59:04.126152	f	f		0					0		0	1503	0	
463	3	320	462	0	458	outbound_desadv	447	5555555555555	1111111111111	outbound_desadv_in		xml	desadv		desadv_xml2edifact	f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:59:09.481829	f	f		0					0		0	0	0	
462	3	310	447	0	458	outbound_desadv	447	5555555555555	1111111111111	outbound_desadv_in		xml	desadv			f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:59:09.411409	f	f		0					0		0	11810	0	
466	3	320	465	0	458	outbound_desadv	449	SENDER	RECEIVER	outbound_desadv_in		xml	desadv		desadv_xml2edifact	f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:59:10.395002	f	f		0					0		0	0	0	
465	3	310	449	0	458	outbound_desadv	449	SENDER	RECEIVER	outbound_desadv_in		xml	desadv			f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:59:10.334693	f	f		0					0		0	1571	0	
472	3	320	471	0	458	outbound_desadv	453	5555555555555	2222222222222	outbound_desadv_in		xml	desadv		desadv_xml2edifact	f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:59:12.813379	f	f		0					0		0	0	0	
469	3	320	468	0	458	outbound_desadv	451	5555555555555	1111111111111	outbound_desadv_in		xml	desadv		desadv_xml2edifact	f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:59:11.776924	f	f		0					0		0	0	0	
471	3	310	453	0	458	outbound_desadv	453	5555555555555	2222222222222	outbound_desadv_in		xml	desadv			f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:59:12.730696	f	f		0					0		0	1503	0	
475	3	320	474	0	458	outbound_desadv	455	6666666666666	1111111111111	outbound_desadv_in		xml	desadv		desadv_xml2edifact	f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:59:14.218741	f	f		0					0		0	0	0	
474	3	310	455	0	458	outbound_desadv	455	6666666666666	1111111111111	outbound_desadv_in		xml	desadv			f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:59:14.031492	f	f		0					0		0	1503	0	
478	3	320	477	0	458	outbound_desadv	457	6666666666666	2222222222222	outbound_desadv_in		xml	desadv		desadv_xml2edifact	f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:59:15.379578	f	f		0					0		0	0	0	
477	3	310	457	0	458	outbound_desadv	457	6666666666666	2222222222222	outbound_desadv_in		xml	desadv			f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:59:15.32488	f	f		0					0		0	1503	0	
457	3	220	456	0	443	outbound_desadv	457			outbound_desadv_in		xml	desadv			f	1						0	f	text/plain	\N	2026-10-11 16:59:04.629364	f	f		0					0		0	1503	0	
458	3	1	0	0	441	outbound_desadv	translate									f	1						0	f	text/plain	\N	2026-10-11 16:59:05.951102	f	f		0					0		0	0	0	
461	3	330	460	480	458	outbound_desadv	461	5555555555555	1111111111111	outbound_desadv_in		edifact	DESADVD96AUNEAN005		desadv_xml2edifact	t	1		46			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:07.643495	f	f		0	edifact				0		0	366	0	
464	3	330	463	480	458	outbound_desadv	464	5555555555555	1111111111111	outbound_desadv_in		edifact	DESADVD96AUNEAN005		desadv_xml2edifact	t	1		47			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:09.667814	f	f		0	edifact				0		0	2793	0	
470	3	330	469	480	458	outbound_desadv	470	5555555555555	1111111111111	outbound_desadv_in		edifact	DESADVD96AUNEAN005		desadv_xml2edifact	t	1		49			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:11.959539	f	f		0	edifact				0		0	495	0	
473	3	330	472	481	458	outbound_desadv	473	5555555555555	2222222222222	outbound_desadv_in		edifact	DESADVD96AUNEAN005		desadv_xml2edifact	t	1		50			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:13.004941	f	f		0	edifact				0		0	495	0	
476	3	330	475	482	458	outbound_desadv	476	6666666666666	1111111111111	outbound_desadv_in		edifact	DESADVD96AUNEAN005		desadv_xml2edifact	t	1		51			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:14.49063	f	f		0	edifact				0		0	495	0	
479	3	330	478	483	458	outbound_desadv	479	6666666666666	2222222222222	outbound_desadv_in		edifact	DESADVD96AUNEAN005		desadv_xml2edifact	t	1		52			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:15.563278	f	f		0	edifact				0		0	495	0	
467	3	330	466	484	458	outbound_desadv	467	SENDER	RECEIVER	outbound_desadv_in		edifact	DESADVD96AUNEAN005		desadv_xml2edifact	t	1		48			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:10.581015	f	f		0	edifact				0		0	495	0	
486	3	500	481	0	441	outbound_desadv	481	5555555555555	2222222222222	outbound_desadv_in	outbound_desadv_out	edifact	DESADVD96AUNEAN005			t	1		6			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:20.358275	f	f		0	edifact				0		0	0	0	
480	3	400	0	0	441	outbound_desadv	480	5555555555555	1111111111111	outbound_desadv_in		edifact	DESADVD96AUNEAN005			t	3		5			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:16.05557	f	f		0	edifact				0		0	3736	0	
481	3	400	0	0	441	outbound_desadv	481	5555555555555	2222222222222	outbound_desadv_in		edifact	DESADVD96AUNEAN005			t	1		6			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:17.513311	f	f		0	edifact				0		0	577	0	
482	3	400	0	0	441	outbound_desadv	482	6666666666666	1111111111111	outbound_desadv_in		edifact	DESADVD96AUNEAN005			t	1		5			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:18.610993	f	f		0	edifact				0		0	577	0	
483	3	400	0	0	441	outbound_desadv	483	6666666666666	2222222222222	outbound_desadv_in		edifact	DESADVD96AUNEAN005			t	1		6			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:19.17325	f	f		0	edifact				0		0	577	0	
484	3	400	0	0	441	outbound_desadv	484	SENDER	RECEIVER	outbound_desadv_in		edifact	DESADVD96AUNEAN005			t	1		3			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:19.638823	f	f		0	edifact				0		0	565	0	
485	3	500	480	0	441	outbound_desadv	480	5555555555555	1111111111111	outbound_desadv_in	outbound_desadv_out	edifact	DESADVD96AUNEAN005			t	3		5			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:20.125091	f	f		0	edifact				0		0	0	0	
501	3	200	0	0	500	outbound_invoice	/o/pg/bots/botssys/infile/edifact_xml/xml/invoicfull01.xml			outbound_invoice_in						f	1						0	f	text/plain	\N	2026-10-11 16:59:29.28574	f	f		0					0		0	0	0	
492	3	520	485	0	491	outbound_desadv	/o/pg/bots/botssys/outfile/edifact_xml/edifact/desadv6.edi	5555555555555	1111111111111	outbound_desadv_in	outbound_desadv_out	edifact	DESADVD96AUNEAN005			t	3		5			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:22.514895	f	f		0	edifact				0		0	0	1	
493	3	520	486	0	491	outbound_desadv	/o/pg/bots/botssys/outfile/edifact_xml/edifact/desadv7.edi	5555555555555	2222222222222	outbound_desadv_in	outbound_desadv_out	edifact	DESADVD96AUNEAN005			t	1		6			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:23.545417	f	f		0	edifact				0		0	0	1	
494	3	520	487	0	491	outbound_desadv	/o/pg/bots/botssys/outfile/edifact_xml/edifact/desadv8.edi	6666666666666	1111111111111	outbound_desadv_in	outbound_desadv_out	edifact	DESADVD96AUNEAN005			t	1		5			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:24.396327	f	f		0	edifact				0		0	0	1	
487	3	500	482	0	441	outbound_desadv	482	6666666666666	1111111111111	outbound_desadv_in	outbound_desadv_out	edifact	DESADVD96AUNEAN005			t	1		5			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:20.588051	f	f		0	edifact				0		0	0	0	
495	3	520	488	0	491	outbound_desadv	/o/pg/bots/botssys/outfile/edifact_xml/edifact/desadv9.edi	6666666666666	2222222222222	outbound_desadv_in	outbound_desadv_out	edifact	DESADVD96AUNEAN005			t	1		6			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:25.267896	f	f		0	edifact				0		0	0	1	
488	3	500	483	0	441	outbound_desadv	483	6666666666666	2222222222222	outbound_desadv_in	outbound_desadv_out	edifact	DESADVD96AUNEAN005			t	1		6			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:21.588476	f	f		0	edifact				0		0	0	0	
496	3	520	489	0	491	outbound_desadv	/o/pg/bots/botssys/outfile/edifact_xml/edifact/desadv10.edi	SENDER	RECEIVER	outbound_desadv_in	outbound_desadv_out	edifact	DESADVD96AUNEAN005			t	1		3			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:26.341353	f	f		0	edifact				0		0	0	1	
489	3	500	484	0	441	outbound_desadv	484	SENDER	RECEIVER	outbound_desadv_in	outbound_desadv_out	edifact	DESADVD96AUNEAN005			t	1		3			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:21.783505	f	f		0	edifact				0		0	0	0	
491	3	1	0	0	490	outbound_desadv	outcommunicate									f	1						0	f	text/plain	\N	2026-10-11 16:59:22.215537	f	f		0					0		0	0	0	
490	3	1	0	0	441	outbound_desadv	run				outbound_desadv_out					f	1						0	f	text/plain	\N	2026-10-11 16:59:21.967356	f	f		0					0		0	0	0	
514	3	310	502	0	513	outbound_invoice	502	5555555555555	1111111111111	outbound_invoice_in		xml	invoice			f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:59:32.71244	f	f		0					0		0	5539	0	
503	3	200	0	0	500	outbound_invoice	/o/pg/bots/botssys/infile/edifact_xml/xml/invoictest01.xml			outbound_invoice_in						f	1						0	f	text/plain	\N	2026-10-11 16:59:29.562855	f	f		0					0		0	0	0	
505	3	200	0	0	500	outbound_invoice	/o/pg/bots/botssys/infile/edifact_xml/xml/invoictest5-1.xml			outbound_invoice_in						f	1						0	f	text/plain	\N	2026-10-11 16:59:30.014981	f	f		0					0		0	0	0	
515	3	320	514	0	513	outbound_invoice	502	5555555555555	1111111111111	outbound_invoice_in		xml	invoice		invoice_xml2edifact	f	1					utf-8	0	f	text/xml 	\N	2026-10-11 16:59:32.887009	f	f		0					0		0	0	0	
507	3	200	0	0	500	outbound_invoice	/o/pg/bots/botssys/infile/edifact_xml/xml/invoictest5-2.xml			outbound_invoice_in						f	1						0	f	text/plain	\N	2026-10-11 16:59:30.738649	f	f		0					0		0	0	0	
509	3	200	0	0	500	outbound_invoice	/o/pg/bots/botssys/infile/edifact_xml/xml/invoictest6-1.xml			outbound_invoice_in						f	1						0	f	text/plain	\N	2026-10-11 16:59:31.194702	f	f		0					0		0	0	0	
502	3	220	501	0	500	outbound_invoice	502			outbound_invoice_in		xml	invoice			f	1						0	f	text/plain	\N	2026-10-11 16:59:29.37165	f	f		0					0		0	5539	0	
511	3	200	0	0	500	outbound_invoice	/o/pg/bots/botssys/infile/edifact_xml/xml/invoictest6-2.xml			outbound_invoice_in						f	1						0	f	text/plain	\N	2026-10-11 16:59:31.686129	f	f		0					0		0	0	0	
500	3	1	0	0	499	outbound_invoice	incommunicate									f	1						0	f	text/plain	\N	2026-10-11 16:59:28.685748	f	f		0					0		0	0	0	
499	3	1	0	0	498	outbound_invoice	run			outbound_invoice_in						f	1						0	f	text/plain	\N	2026-10-11 16:59:28.387939	f	f		0					0		0	0	0	
504	3	220	503	0	500	outbound_invoice	504			outbound_invoice_in		xml	invoice			f	1						0	f	text/plain	\N	2026-10-11 16:59:29.656998	f	f		0					0		0	2196	0	
506	3	220	505	0	500	outbound_invoice	506			outbound_invoice_in		xml	invoice			f	1						0	f	text/plain	\N	2026-10-11 16:59:30.147688	f	f		0					0		0	2208	0	
508	3	220	507	0	500	outbound_invoice	508			outbound_invoice_in		xml	invoice			f	1						0	f	text/plain	\N	2026-10-11 16:59:30.792745	f	f		0					0		0	2208	0	
510	3	220	509	0	500	outbound_invoice	510			outbound_invoice_in		xml	invoice			f	1						0	f	text/plain	\N	2026-10-11 16:59:31.287211	f	f		0					0		0	2208	0	
512	3	220	511	0	500	outbound_invoice	512			outbound_invoice_in		xml	invoice			f	1						0	f	text/plain	\N	2026-10-11 16:59:31.920963	f	f		0					0		0	2208	0	
513	3	1	0	0	498	outbound_invoice	translate									f	1						0	f	text/plain	\N	2026-10-11 16:59:32.63033	f	f		0					0		0	0	0	
516	3	330	515	532	513	outbound_invoice	516	5555555555555	1111111111111	outbound_invoice_in		edifact	INVOICD96AUNEAN008		invoice_xml2edifact	t	1		53			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:33.119765	f	f		0	edifact				0		0	1579	0	
522	3	330	521	532	513	outbound_invoice	522	5555555555555	1111111111111	outbound_invoice_in		edifact	INVOICD96AUNEAN008		invoice_xml2edifact	t	1		55			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:37.04759	f	f		0	edifact				0		0	744	0	
532	3	400	0	0	498	outbound_invoice	532	5555555555555	1111111111111	outbound_invoice_in		edifact	INVOICD96AUNEAN008			t	2		7			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:41.413685	f	f		0	edifact				0		0	2405	0	
498	3	1	0	0	497	outbound_invoice	routepart									f	1						0	f	text/plain	\N	2026-10-11 16:59:28.168919	f	f		0					0		0	0	0	
497	3	1	0	0	276	outbound_invoice	router									f	1						0	f	text/plain	\N	2026-10-11 16:59:28.066118	f	f		0					0		0	0	0	
525	3	330	524	533	513	outbound_invoice	525	5555555555555	2222222222222	outbound_invoice_in		edifact	INVOICD96AUNEAN008		invoice_xml2edifact	t	1		56			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:38.752273	f	f		0	edifact				0		0	744	0	
531	3	330	530	535	513	outbound_invoice	531	6666666666666	2222222222222	outbound_invoice_in		edifact	INVOICD96AUNEAN008		invoice_xml2edifact	t	1		58			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:40.599116	f	f		0	edifact				0		0	744	0	
543	3	1	0	0	542	outbound_invoice	outcommunicate									f	1						0	f	text/plain	\N	2026-10-11 16:59:46.200692	f	f		0					0		0	0	0	
542	3	1	0	0	498	outbound_invoice	run				outbound_invoice_out					f	1						0	f	text/plain	\N	2026-10-11 16:59:45.715442	f	f		0					0		0	0	0	
534	3	400	0	0	498	outbound_invoice	534	6666666666666	1111111111111	outbound_invoice_in		edifact	INVOICD96AUNEAN008			t	1		7			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:42.819925	f	f		0	edifact				0		0	826	0	
535	3	400	0	0	498	outbound_invoice	535	6666666666666	2222222222222	outbound_invoice_in		edifact	INVOICD96AUNEAN008			t	1		8			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:43.181855	f	f		0	edifact				0		0	826	0	
536	3	400	0	0	498	outbound_invoice	536	SENDER	RECEIVER	outbound_invoice_in		edifact	INVOICD96AUNEAN008			t	1		4			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:43.557671	f	f		0	edifact				0		0	814	0	
544	3	520	537	0	543	outbound_invoice	/o/pg/bots/botssys/outfile/edifact_xml/edifact/invoic6.edi	5555555555555	1111111111111	outbound_invoice_in	outbound_invoice_out	edifact	INVOICD96AUNEAN008			t	2		7			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:46.301814	f	f		0	edifact				0		0	0	1	
537	3	500	532	0	498	outbound_invoice	532	5555555555555	1111111111111	outbound_invoice_in	outbound_invoice_out	edifact	INVOICD96AUNEAN008			t	2		7			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:44.195782	f	f		0	edifact				0		0	0	0	
545	3	520	538	0	543	outbound_invoice	/o/pg/bots/botssys/outfile/edifact_xml/edifact/invoic7.edi	5555555555555	2222222222222	outbound_invoice_in	outbound_invoice_out	edifact	INVOICD96AUNEAN008			t	1		8			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:47.183528	f	f		0	edifact				0		0	0	1	
538	3	500	533	0	498	outbound_invoice	533	5555555555555	2222222222222	outbound_invoice_in	outbound_invoice_out	edifact	INVOICD96AUNEAN008			t	1		8			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:44.571242	f	f		0	edifact				0		0	0	0	
546	3	520	539	0	543	outbound_invoice	/o/pg/bots/botssys/outfile/edifact_xml/edifact/invoic8.edi	6666666666666	1111111111111	outbound_invoice_in	outbound_invoice_out	edifact	INVOICD96AUNEAN008			t	1		7			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:47.898263	f	f		0	edifact				0		0	0	1	
539	3	500	534	0	498	outbound_invoice	534	6666666666666	1111111111111	outbound_invoice_in	outbound_invoice_out	edifact	INVOICD96AUNEAN008			t	1		7			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:44.834154	f	f		0	edifact				0		0	0	0	
547	3	520	540	0	543	outbound_invoice	/o/pg/bots/botssys/outfile/edifact_xml/edifact/invoic9.edi	6666666666666	2222222222222	outbound_invoice_in	outbound_invoice_out	edifact	INVOICD96AUNEAN008			t	1		8			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:48.410066	f	f		0	edifact				0		0	0	1	
540	3	500	535	0	498	outbound_invoice	535	6666666666666	2222222222222	outbound_invoice_in	outbound_invoice_out	edifact	INVOICD96AUNEAN008			t	1		8			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:45.041425	f	f		0	edifact				0		0	0	0	
548	3	520	541	0	543	outbound_invoice	/o/pg/bots/botssys/outfile/edifact_xml/edifact/invoic10.edi	SENDER	RECEIVER	outbound_invoice_in	outbound_invoice_out	edifact	INVOICD96AUNEAN008			t	1		4			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:48.796334	f	f		0	edifact				0		0	0	1	
541	3	500	536	0	498	outbound_invoice	536	SENDER	RECEIVER	outbound_invoice_in	outbound_invoice_out	edifact	INVOICD96AUNEAN008			t	1		4			UNOC	0	f	application/EDIFACT	\N	2026-10-11 16:59:45.263478	f	f		0	edifact				0		0	0	0	
554	3	200	0	0	553	demo_partner_conversion	/o/pg/bots/botssys/infile/demo_work_with_partners/partner_conversion/frompartner1_topartner1_1.x12			demo_partner_conversion_in						f	1						0	f	text/plain	\N	2026-10-12 03:50:49.103872	f	f		0					0		0	0	0	
553	3	1	0	0	552	demo_partner_conversion	incommunicate									f	1						0	f	text/plain	\N	2026-10-12 03:50:49.085488	f	f		0					0		0	0	0	
552	3	1	0	0	551	demo_partner_conversion	run			demo_partner_conversion_in						f	1						0	f	text/plain	\N	2026-10-12 03:50:49.046861	f	f		0					0		0	0	0	
573	3	200	0	0	570	inbound_orders	/o/pg/bots/botssys/infile/edifact_xml/edifact/0T0000000015.edi			inbound_orders_in						f	1						0	f	text/plain	\N	2026-10-12 03:50:50.725902	f	f		0					0		0	0	0	
555	3	220	554	0	553	demo_partner_conversion	555			demo_partner_conversion_in		x12	x12			f	1						0	f	text/plain	\N	2026-10-12 03:50:49.109544	f	f		0					0		0	1229	0	
556	3	1	0	0	551	demo_partner_conversion	preprocess									f	1						0	f	text/plain	\N	2026-10-12 03:50:49.20734	f	f		0					0		0	0	0	
560	3	320	559	0	558	demo_partner_conversion	557	FROMPARTNER2	TOPARTNER2	demo_partner_conversion_in		x12	856004010		inn2out	t	1	P	0004			us-ascii	0	f	application/X12	\N	2026-10-12 03:50:49.926053	f	f		0	x12				0		0	0	0	
559	3	310	557	0	558	demo_partner_conversion	557	FROMPARTNER2	TOPARTNER2	demo_partner_conversion_in		x12	x12			t	1	P				us-ascii	0	f	application/X12	\N	2026-10-12 03:50:49.277558	f	f		0	x12				0		0	1227	0	
557	3	220	555	0	556	demo_partner_conversion	557			demo_partner_conversion_in		x12	x12			f	1						0	f	text/plain	\N	2026-10-12 03:50:49.21303	f	f		0					0		0	1227	0	
558	3	1	0	0	551	demo_partner_conversion	translate									f	1						0	f	text/plain	\N	2026-10-12 03:50:49.254282	f	f		0					0		0	0	0	
561	3	330	560	562	558	demo_partner_conversion	561	FROMPARTNER2	TOPARTNER2	demo_partner_conversion_in		x12	856004010		inn2out	t	1	P	59			us-ascii	0	f	application/X12	\N	2026-10-12 03:50:49.999357	f	f		0	x12				0		0	1037	0	
562	3	400	0	0	551	demo_partner_conversion	562	frompartner1	topartner1	demo_partner_conversion_in		x12	856004010			t	1	P	3			us-ascii	0	f	application/X12	\N	2026-10-12 03:50:50.288286	f	f		0	x12				0		0	1227	0	
566	3	520	563	0	565	demo_partner_conversion	/o/pg/bots/botssys/outfile/demo_work_with_partners/partner_conversion/frompartner1_topartner1_3.x12	frompartner1	topartner1	demo_partner_conversion_in	demo_partner_conversion_out	x12	856004010			t	1	P	3			us-ascii	0	f	application/X12	\N	2026-10-12 03:50:50.453774	f	f		0	x12				0		0	0	1	
563	3	500	562	0	551	demo_partner_conversion	562	frompartner1	topartner1	demo_partner_conversion_in	demo_partner_conversion_out	x12	856004010			t	1	P	3			us-ascii	0	f	application/X12	\N	2026-10-12 03:50:50.376539	f	f		0	x12				0		0	0	0	
565	3	1	0	0	564	demo_partner_conversion	outcommunicate									f	1						0	f	text/plain	\N	2026-10-12 03:50:50.435237	f	f		0					0		0	0	0	
564	3	1	0	0	551	demo_partner_conversion	run				demo_partner_conversion_out					f	1						0	f	text/plain	\N	2026-10-12 03:50:50.410593	f	f		0					0		0	0	0	
550	3	1	0	0	549	demo_partner_conversion	router									f	1						0	f	text/plain	\N	2026-10-12 03:50:48.994428	f	f		0					0		0	0	0	
581	3	220	572	0	579	inbound_orders	581			inbound_orders_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-12 03:50:50.886568	f	f		0					0		0	286	0	
571	3	200	0	0	570	inbound_orders	/o/pg/bots/botssys/infile/edifact_xml/edifact/0T0000000004.edi			inbound_orders_in						f	1						0	f	text/plain	\N	2026-10-12 03:50:50.686642	f	f		0					0		0	0	0	
582	3	220	574	0	579	inbound_orders	582			inbound_orders_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-12 03:50:50.905229	f	f		0					0		0	261	0	
575	3	200	0	0	570	inbound_orders	/o/pg/bots/botssys/infile/edifact_xml/edifact/T0000000001.edi			inbound_orders_in						f	1						0	f	text/plain	\N	2026-10-12 03:50:50.759433	f	f		0					0		0	0	0	
572	3	220	571	0	570	inbound_orders	572			inbound_orders_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-12 03:50:50.694698	f	f		0					0		0	779	0	
577	3	200	0	0	570	inbound_orders	/o/pg/bots/botssys/infile/edifact_xml/edifact/T0000000002.edi			inbound_orders_in						f	1						0	f	text/plain	\N	2026-10-12 03:50:50.78515	f	f		0					0		0	0	0	
570	3	1	0	0	569	inbound_orders	incommunicate									f	1						0	f	text/plain	\N	2026-10-12 03:50:50.669598	f	f		0					0		0	0	0	
569	3	1	0	0	568	inbound_orders	run			inbound_orders_in						f	1						0	f	text/plain	\N	2026-10-12 03:50:50.643558	f	f		0					0		0	0	0	
579	3	1	0	0	568	inbound_orders	preprocess									f	1						0	f	text/plain	\N	2026-10-12 03:50:50.859232	f	f		0					0		0	0	0	
583	3	220	576	0	579	inbound_orders	583			inbound_orders_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-12 03:50:50.931682	f	f		0					0		0	276	0	
574	3	220	573	0	570	inbound_orders	574			inbound_orders_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-12 03:50:50.735438	f	f		0					0		0	262	0	
584	3	220	578	0	579	inbound_orders	584			inbound_orders_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-12 03:50:50.94852	f	f		0					0		0	282	0	
576	3	220	575	0	570	inbound_orders	576			inbound_orders_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-12 03:50:50.765803	f	f		0					0		0	278	0	
585	3	1	0	0	568	inbound_orders	translate									f	1						0	f	text/plain	\N	2026-10-12 03:50:51.00253	f	f		0					0		0	0	0	
578	3	220	577	0	570	inbound_orders	578			inbound_orders_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-12 03:50:50.79171	f	f		0					0		0	284	0	
586	3	310	580	0	585	inbound_orders	580	PARTNER1	PARTNER2	inbound_orders_in		edifact	edifact			t	1					UNOA	0	f	application/EDIFACT	\N	2026-10-12 03:50:51.025821	f	f		0	edifact				0		0	489	0	
580	3	220	572	0	579	inbound_orders	580			inbound_orders_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-12 03:50:50.864041	f	f		0					0		0	489	0	
568	3	1	0	0	567	inbound_orders	routepart									f	1						0	f	text/plain	\N	2026-10-12 03:50:50.629385	f	f		0					0		0	0	0	
567	3	1	0	0	549	inbound_orders	router									f	1						0	f	text/plain	\N	2026-10-12 03:50:50.542986	f	f		0					0		0	0	0	
590	3	330	589	0	585	inbound_orders	590	PARTNER1	PARTNER2	inbound_orders_in		xml	orders		orders_edifact2xml	f	1		T0000000004-2			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:51.192808	f	f		0					0		0	586	0	
587	3	320	586	0	585	inbound_orders	580	PARTNER1	PARTNER2	inbound_orders_in		edifact	ORDERSD96AUNEAN008		orders_edifact2xml	t	1		T0000000004-1			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:51.103657	f	f		0	edifact				0		0	0	0	
602	3	330	601	0	585	inbound_orders	602	PARTNER1	PARTNER2	inbound_orders_in		xml	orders		orders_edifact2xml	f	1		T0000000002-1			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:51.432986	f	f		0					0		0	586	0	
589	3	320	586	0	585	inbound_orders	580	PARTNER1	PARTNER2	inbound_orders_in		edifact	ORDERSD96AUNEAN008		orders_edifact2xml	t	1		T0000000004-2			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:51.183303	f	f		0	edifact				0		0	0	0	
598	3	320	597	0	585	inbound_orders	583	PARTNER1	PARTNER2	inbound_orders_in		edifact	ORDERSD96AUNEAN008		orders_edifact2xml	t	1		T0000000001			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:51.373779	f	f		0	edifact				0		0	0	0	
592	3	320	591	0	585	inbound_orders	581	PARTNER1	PARTNER2	inbound_orders_in		edifact	ORDERSD96AUNEAN008		orders_edifact2xml	t	1		T0000000004-3			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:51.252041	f	f		0	edifact				0		0	0	0	
591	3	310	581	0	585	inbound_orders	581	PARTNER1	PARTNER2	inbound_orders_in		edifact	edifact			t	1					UNOA	0	f	application/EDIFACT	\N	2026-10-12 03:50:51.243473	f	f		0	edifact				0		0	286	0	
597	3	310	583	0	585	inbound_orders	583	PARTNER1	PARTNER2	inbound_orders_in		edifact	edifact			t	1					UNOA	0	f	application/EDIFACT	\N	2026-10-12 03:50:51.36562	f	f		0	edifact				0		0	276	0	
603	3	400	588	0	568	inbound_orders	588	PARTNER1	PARTNER2	inbound_orders_in		xml	orders			f	1		T0000000004-1			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:51.483039	f	f		0					0		0	586	0	
595	3	320	594	0	585	inbound_orders	582	PARTNER1	PARTNER2	inbound_orders_in		edifact	ORDERSD96AUNEAN008		orders_edifact2xml	t	1		T0000000015			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:51.315584	f	f		0	edifact				0		0	0	0	
594	3	310	582	0	585	inbound_orders	582	PARTNER1	PARTNER2	inbound_orders_in		edifact	edifact			t	1					UNOA	0	f	application/EDIFACT	\N	2026-10-12 03:50:51.306996	f	f		0	edifact				0		0	261	0	
612	3	500	606	0	568	inbound_orders	596	PARTNER1	PARTNER2	inbound_orders_in	inbound_orders_out	xml	orders			f	1		T0000000015			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:51.653307	f	f		0					0		0	0	0	
601	3	320	600	0	585	inbound_orders	584	PARTNER1	PARTNER2	inbound_orders_in		edifact	ORDERSD96AUNEAN008		orders_edifact2xml	t	1		T0000000002-1			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:51.423577	f	f		0	edifact				0		0	0	0	
600	3	310	584	0	585	inbound_orders	584	PARTNER1	PARTNER2	inbound_orders_in		edifact	edifact			t	1					UNOA	0	f	application/EDIFACT	\N	2026-10-12 03:50:51.415057	f	f		0	edifact				0		0	282	0	
605	3	400	593	0	568	inbound_orders	593	PARTNER1	PARTNER2	inbound_orders_in		xml	orders			f	1		T0000000004-3			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:51.517362	f	f		0					0		0	586	0	
588	3	330	587	0	585	inbound_orders	588	PARTNER1	PARTNER2	inbound_orders_in		xml	orders		orders_edifact2xml	f	1		T0000000004-1			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:51.134892	f	f		0					0		0	586	0	
593	3	330	592	0	585	inbound_orders	593	PARTNER1	PARTNER2	inbound_orders_in		xml	orders		orders_edifact2xml	f	1		T0000000004-3			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:51.263072	f	f		0					0		0	586	0	
614	3	500	608	0	568	inbound_orders	602	PARTNER1	PARTNER2	inbound_orders_in	inbound_orders_out	xml	orders			f	1		T0000000002-1			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:51.681456	f	f		0					0		0	0	0	
596	3	330	595	0	585	inbound_orders	596	PARTNER1	PARTNER2	inbound_orders_in		xml	orders		orders_edifact2xml	f	1		T0000000015			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:51.328556	f	f		0					0		0	584	0	
616	3	1	0	0	615	inbound_orders	outcommunicate									f	1						0	f	text/plain	\N	2026-10-12 03:50:51.711229	f	f		0					0		0	0	0	
599	3	330	598	0	585	inbound_orders	599	PARTNER1	PARTNER2	inbound_orders_in		xml	orders		orders_edifact2xml	f	1		T0000000001			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:51.3845	f	f		0					0		0	584	0	
611	3	500	605	0	568	inbound_orders	593	PARTNER1	PARTNER2	inbound_orders_in	inbound_orders_out	xml	orders			f	1		T0000000004-3			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:51.637527	f	f		0					0		0	0	0	
604	3	400	590	0	568	inbound_orders	590	PARTNER1	PARTNER2	inbound_orders_in		xml	orders			f	1		T0000000004-2			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:51.499117	f	f		0					0		0	586	0	
613	3	500	607	0	568	inbound_orders	599	PARTNER1	PARTNER2	inbound_orders_in	inbound_orders_out	xml	orders			f	1		T0000000001			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:51.667757	f	f		0					0		0	0	0	
606	3	400	596	0	568	inbound_orders	596	PARTNER1	PARTNER2	inbound_orders_in		xml	orders			f	1		T0000000015			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:51.533882	f	f		0					0		0	584	0	
607	3	400	599	0	568	inbound_orders	599	PARTNER1	PARTNER2	inbound_orders_in		xml	orders			f	1		T0000000001			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:51.553231	f	f		0					0		0	584	0	
608	3	400	602	0	568	inbound_orders	602	PARTNER1	PARTNER2	inbound_orders_in		xml	orders			f	1		T0000000002-1			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:51.576138	f	f		0					0		0	586	0	
617	3	520	609	0	616	inbound_orders	/o/pg/bots/botssys/outfile/edifact_xml/xml/orders_13.xml	PARTNER1	PARTNER2	inbound_orders_in	inbound_orders_out	xml	orders			f	1		T0000000004-1			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:51.717718	f	f		0					0		0	0	1	
609	3	500	603	0	568	inbound_orders	588	PARTNER1	PARTNER2	inbound_orders_in	inbound_orders_out	xml	orders			f	1		T0000000004-1			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:51.597177	f	f		0					0		0	0	0	
610	3	500	604	0	568	inbound_orders	590	PARTNER1	PARTNER2	inbound_orders_in	inbound_orders_out	xml	orders			f	1		T0000000004-2			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:51.616907	f	f		0					0		0	0	0	
615	3	1	0	0	568	inbound_orders	run				inbound_orders_out					f	1						0	f	text/plain	\N	2026-10-12 03:50:51.695201	f	f		0					0		0	0	0	
684	3	320	683	0	682	outbound_asn	675	SENDER	PARTNER1	outbound_asn_in		xml	asn		asn_xml2x12_default	f	1	P				utf-8	0	f	text/xml 	\N	2026-10-12 03:50:53.136345	f	f		0					0		0	0	0	
618	3	520	610	0	616	inbound_orders	/o/pg/bots/botssys/outfile/edifact_xml/xml/orders_14.xml	PARTNER1	PARTNER2	inbound_orders_in	inbound_orders_out	xml	orders			f	1		T0000000004-2			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:51.744551	f	f		0					0		0	0	1	
619	3	520	611	0	616	inbound_orders	/o/pg/bots/botssys/outfile/edifact_xml/xml/orders_15.xml	PARTNER1	PARTNER2	inbound_orders_in	inbound_orders_out	xml	orders			f	1		T0000000004-3			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:51.772361	f	f		0					0		0	0	1	
620	3	520	612	0	616	inbound_orders	/o/pg/bots/botssys/outfile/edifact_xml/xml/orders_16.xml	PARTNER1	PARTNER2	inbound_orders_in	inbound_orders_out	xml	orders			f	1		T0000000015			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:51.797603	f	f		0					0		0	0	1	
621	3	520	613	0	616	inbound_orders	/o/pg/bots/botssys/outfile/edifact_xml/xml/orders_17.xml	PARTNER1	PARTNER2	inbound_orders_in	inbound_orders_out	xml	orders			f	1		T0000000001			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:51.829628	f	f		0					0		0	0	1	
622	3	520	614	0	616	inbound_orders	/o/pg/bots/botssys/outfile/edifact_xml/xml/orders_18.xml	PARTNER1	PARTNER2	inbound_orders_in	inbound_orders_out	xml	orders			f	1		T0000000002-1			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:51.855682	f	f		0					0		0	0	1	
627	3	200	0	0	626	myfirstroute	/o/pg/bots/botssys/infile/my_first_plugin/order01.edi			myfirstroute_in						f	1						0	f	text/plain	\N	2026-10-12 03:50:51.934208	f	f		0					0		0	0	0	
628	3	220	627	0	626	myfirstroute	628			myfirstroute_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-12 03:50:51.940518	f	f		0					0		0	920	0	
629	3	200	0	0	626	myfirstroute	/o/pg/bots/botssys/infile/my_first_plugin/order02.edi			myfirstroute_in						f	1						0	f	text/plain	\N	2026-10-12 03:50:51.957258	f	f		0					0		0	0	0	
631	3	200	0	0	626	myfirstroute	/o/pg/bots/botssys/infile/my_first_plugin/order03.edi			myfirstroute_in						f	1						0	f	text/plain	\N	2026-10-12 03:50:51.982854	f	f		0					0		0	0	0	
626	3	1	0	0	625	myfirstroute	incommunicate									f	1						0	f	text/plain	\N	2026-10-12 03:50:51.926282	f	f		0					0		0	0	0	
625	3	1	0	0	624	myfirstroute	run			myfirstroute_in						f	1						0	f	text/plain	\N	2026-10-12 03:50:51.912112	f	f		0					0		0	0	0	
640	3	320	639	0	638	myfirstroute	634	8712345678906	PARTNER2	myfirstroute_in		edifact	ORDERSD96AUNEAN008		orders_edifact2xml	t	1		T0000000004-1			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:52.184187	f	f		0	edifact				0		0	0	0	
630	3	220	629	0	626	myfirstroute	630			myfirstroute_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-12 03:50:51.962515	f	f		0					0		0	270	0	
638	3	1	0	0	624	myfirstroute	translate									f	1						0	f	text/plain	\N	2026-10-12 03:50:52.127831	f	f		0					0		0	0	0	
632	3	220	631	0	626	myfirstroute	632			myfirstroute_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-12 03:50:51.988346	f	f		0					0		0	267	0	
633	3	1	0	0	624	myfirstroute	preprocess									f	1						0	f	text/plain	\N	2026-10-12 03:50:52.022168	f	f		0					0		0	0	0	
634	3	220	628	0	633	myfirstroute	634			myfirstroute_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-12 03:50:52.027813	f	f		0					0		0	500	0	
642	3	320	639	0	638	myfirstroute	634	8712345678906	PARTNER2	myfirstroute_in		edifact	ORDERSD96AUNEAN008		orders_edifact2xml	t	1		T0000000004-2			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:52.230236	f	f		0	edifact				0		0	0	0	
639	3	310	634	0	638	myfirstroute	634	8712345678906	PARTNER2	myfirstroute_in		edifact	edifact			t	1					UNOA	0	f	application/EDIFACT	\N	2026-10-12 03:50:52.142637	f	f		0	edifact				0		0	500	0	
635	3	220	628	0	633	myfirstroute	635			myfirstroute_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-12 03:50:52.042335	f	f		0					0		0	416	0	
645	3	320	644	0	638	myfirstroute	635	8712345678906	PARTNER2	myfirstroute_in		edifact	ORDERSD96AUNEAN008		orders_edifact2xml	t	1		T0000000004-3			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:52.307483	f	f		0	edifact				0		0	0	0	
644	3	310	635	0	638	myfirstroute	635	8712345678906	PARTNER2	myfirstroute_in		edifact	edifact			t	1					UNOA	0	f	application/EDIFACT	\N	2026-10-12 03:50:52.299109	f	f		0	edifact				0		0	416	0	
648	3	320	647	0	638	myfirstroute	636	8712345678906	PARTNER2	myfirstroute_in		edifact	ORDERSD96AUNEAN008		orders_edifact2xml	t	1		T0000000015			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:52.3922	f	f		0	edifact				0		0	0	0	
647	3	310	636	0	638	myfirstroute	636	8712345678906	PARTNER2	myfirstroute_in		edifact	edifact			t	1					UNOA	0	f	application/EDIFACT	\N	2026-10-12 03:50:52.37007	f	f		0	edifact				0		0	269	0	
636	3	220	630	0	633	myfirstroute	636			myfirstroute_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-12 03:50:52.060262	f	f		0					0		0	269	0	
650	3	310	637	0	638	myfirstroute	637	8712345678906	PARTNER2	myfirstroute_in		edifact	edifact			t	1					UNOA	0	f	application/EDIFACT	\N	2026-10-12 03:50:52.447314	f	f		0	edifact				0		0	265	0	
637	3	220	632	0	633	myfirstroute	637			myfirstroute_in		edifact	edifact			f	1						0	f	text/plain	\N	2026-10-12 03:50:52.077123	f	f		0					0		0	265	0	
641	3	330	640	0	638	myfirstroute	641	8712345678906	PARTNER2	myfirstroute_in		xml	orders		orders_edifact2xml	f	1		ORDT0000000004-1			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:52.196531	f	f		0					0		0	594	0	
643	3	330	642	0	638	myfirstroute	643	8712345678906	PARTNER2	myfirstroute_in		xml	orders		orders_edifact2xml	f	1		ORDT0000000004-2			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:52.24148	f	f		0					0		0	594	0	
646	3	330	645	0	638	myfirstroute	646	8712345678906	PARTNER2	myfirstroute_in		xml	orders		orders_edifact2xml	f	1		ORDT0000000004-3			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:52.318311	f	f		0					0		0	1006	0	
649	3	330	648	0	638	myfirstroute	649	8712345678906	PARTNER2	myfirstroute_in		xml	orders		orders_edifact2xml	f	1		ORDT0000000015			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:52.404095	f	f		0					0		0	592	0	
624	3	1	0	0	623	myfirstroute	routepart									f	1						0	f	text/plain	\N	2026-10-12 03:50:51.9056	f	f		0					0		0	0	0	
623	3	1	0	0	549	myfirstroute	router									f	1						0	f	text/plain	\N	2026-10-12 03:50:51.900003	f	f		0					0		0	0	0	
675	3	220	674	0	673	outbound_asn	675			outbound_asn_in		xml	asn			f	1						0	f	text/plain	\N	2026-10-12 03:50:52.994373	f	f		0					0		0	16468	0	
651	3	320	650	0	638	myfirstroute	637	8712345678906	PARTNER2	myfirstroute_in		edifact	ORDERSD96AUNEAN008		orders_edifact2xml	t	1		T0000000001			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:52.456478	f	f		0	edifact				0		0	0	0	
665	3	520	658	0	664	myfirstroute	/o/pg/bots/botssys/outfile/my_first_plugin/orders11.inh	8712345678906	PARTNER2	myfirstroute_in	myfirstroute_out	xml	orders			f	1		ORDT0000000004-1			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:52.787967	f	f		0					0		0	0	1	
658	3	500	653	0	624	myfirstroute	641	8712345678906	PARTNER2	myfirstroute_in	myfirstroute_out	xml	orders			f	1		ORDT0000000004-1			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:52.672935	f	f		0					0		0	0	0	
652	3	330	651	0	638	myfirstroute	652	8712345678906	PARTNER2	myfirstroute_in		xml	orders		orders_edifact2xml	f	1		ORDT0000000001			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:52.471277	f	f		0					0		0	592	0	
664	3	1	0	0	663	myfirstroute	outcommunicate									f	1						0	f	text/plain	\N	2026-10-12 03:50:52.782777	f	f		0					0		0	0	0	
653	3	400	641	0	624	myfirstroute	641	8712345678906	PARTNER2	myfirstroute_in		xml	orders			f	1		ORDT0000000004-1			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:52.52687	f	f		0					0		0	594	0	
663	3	1	0	0	624	myfirstroute	run				myfirstroute_out					f	1						0	f	text/plain	\N	2026-10-12 03:50:52.769572	f	f		0					0		0	0	0	
654	3	400	643	0	624	myfirstroute	643	8712345678906	PARTNER2	myfirstroute_in		xml	orders			f	1		ORDT0000000004-2			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:52.567043	f	f		0					0		0	594	0	
655	3	400	646	0	624	myfirstroute	646	8712345678906	PARTNER2	myfirstroute_in		xml	orders			f	1		ORDT0000000004-3			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:52.609568	f	f		0					0		0	1006	0	
656	3	400	649	0	624	myfirstroute	649	8712345678906	PARTNER2	myfirstroute_in		xml	orders			f	1		ORDT0000000015			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:52.629101	f	f		0					0		0	592	0	
657	3	400	652	0	624	myfirstroute	652	8712345678906	PARTNER2	myfirstroute_in		xml	orders			f	1		ORDT0000000001			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:52.651082	f	f		0					0		0	592	0	
666	3	520	659	0	664	myfirstroute	/o/pg/bots/botssys/outfile/my_first_plugin/orders12.inh	8712345678906	PARTNER2	myfirstroute_in	myfirstroute_out	xml	orders			f	1		ORDT0000000004-2			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:52.814	f	f		0					0		0	0	1	
659	3	500	654	0	624	myfirstroute	643	8712345678906	PARTNER2	myfirstroute_in	myfirstroute_out	xml	orders			f	1		ORDT0000000004-2			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:52.697912	f	f		0					0		0	0	0	
667	3	520	660	0	664	myfirstroute	/o/pg/bots/botssys/outfile/my_first_plugin/orders13.inh	8712345678906	PARTNER2	myfirstroute_in	myfirstroute_out	xml	orders			f	1		ORDT0000000004-3			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:52.838236	f	f		0					0		0	0	1	
660	3	500	655	0	624	myfirstroute	646	8712345678906	PARTNER2	myfirstroute_in	myfirstroute_out	xml	orders			f	1		ORDT0000000004-3			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:52.719757	f	f		0					0		0	0	0	
668	3	520	661	0	664	myfirstroute	/o/pg/bots/botssys/outfile/my_first_plugin/orders14.inh	8712345678906	PARTNER2	myfirstroute_in	myfirstroute_out	xml	orders			f	1		ORDT0000000015			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:52.86307	f	f		0					0		0	0	1	
661	3	500	656	0	624	myfirstroute	649	8712345678906	PARTNER2	myfirstroute_in	myfirstroute_out	xml	orders			f	1		ORDT0000000015			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:52.735094	f	f		0					0		0	0	0	
669	3	520	662	0	664	myfirstroute	/o/pg/bots/botssys/outfile/my_first_plugin/orders15.inh	8712345678906	PARTNER2	myfirstroute_in	myfirstroute_out	xml	orders			f	1		ORDT0000000001			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:52.886833	f	f		0					0		0	0	1	
662	3	500	657	0	624	myfirstroute	652	8712345678906	PARTNER2	myfirstroute_in	myfirstroute_out	xml	orders			f	1		ORDT0000000001			utf-8	0	f	text/xml 	\N	2026-10-12 03:50:52.754884	f	f		0					0		0	0	0	
677	3	220	676	0	673	outbound_asn	677			outbound_asn_in		xml	asn			f	1						0	f	text/plain	\N	2026-10-12 03:50:53.029141	f	f		0					0		0	4523	0	
679	3	220	678	0	673	outbound_asn	679			outbound_asn_in		xml	asn			f	1						0	f	text/plain	\N	2026-10-12 03:50:53.049822	f	f		0					0		0	1192	0	
674	3	200	0	0	673	outbound_asn	/o/pg/bots/botssys/infile/demo_work_with_partners/asn/856_PARTNER1_03.xml			outbound_asn_in						f	1						0	f	text/plain	\N	2026-10-12 03:50:52.987153	f	f		0					0		0	0	0	
676	3	200	0	0	673	outbound_asn	/o/pg/bots/botssys/infile/demo_work_with_partners/asn/856_PARTNER2_01.xml			outbound_asn_in						f	1						0	f	text/plain	\N	2026-10-12 03:50:53.022666	f	f		0					0		0	0	0	
681	3	220	680	0	673	outbound_asn	681			outbound_asn_in		xml	asn			f	1						0	f	text/plain	\N	2026-10-12 03:50:53.071659	f	f		0					0		0	3396	0	
678	3	200	0	0	673	outbound_asn	/o/pg/bots/botssys/infile/demo_work_with_partners/asn/856_PARTNER2_04.xml			outbound_asn_in						f	1						0	f	text/plain	\N	2026-10-12 03:50:53.044303	f	f		0					0		0	0	0	
671	3	1	0	0	670	outbound_asn	routepart									f	1						0	f	text/plain	\N	2026-10-12 03:50:52.952109	f	f		0					0		0	0	0	
680	3	200	0	0	673	outbound_asn	/o/pg/bots/botssys/infile/demo_work_with_partners/asn/856_PARTNER3_02.xml			outbound_asn_in						f	1						0	f	text/plain	\N	2026-10-12 03:50:53.066839	f	f		0					0		0	0	0	
673	3	1	0	0	672	outbound_asn	incommunicate									f	1						0	f	text/plain	\N	2026-10-12 03:50:52.97431	f	f		0					0		0	0	0	
672	3	1	0	0	671	outbound_asn	run			outbound_asn_in						f	1						0	f	text/plain	\N	2026-10-12 03:50:52.960009	f	f		0					0		0	0	0	
670	3	1	0	0	549	outbound_asn	router									f	1						0	f	text/plain	\N	2026-10-12 03:50:52.938499	f	f		0					0		0	0	0	
683	3	310	675	0	682	outbound_asn	675	SENDER	PARTNER1	outbound_asn_in		xml	asn			f	1	P				utf-8	0	f	text/xml 	\N	2026-10-12 03:50:53.114128	f	f		0					0		0	16468	0	
687	3	320	686	0	682	outbound_asn	677	SENDER	PARTNER2	outbound_asn_in		xml	asn		asn_xml2x12_partner2	f	1	P				utf-8	0	f	text/xml 	\N	2026-10-12 03:50:53.281986	f	f		0					0		0	0	0	
686	3	310	677	0	682	outbound_asn	677	SENDER	PARTNER2	outbound_asn_in		xml	asn			f	1	P				utf-8	0	f	text/xml 	\N	2026-10-12 03:50:53.273622	f	f		0					0		0	4523	0	
694	3	330	693	697	682	outbound_asn	694	SENDER	PARTNER3	outbound_asn_in		x12	856004010		asn_xml2x12_noSSCC	t	1	P	74			us-ascii	0	f	application/X12	\N	2026-10-12 03:50:53.436435	f	f		0	x12				0		0	1037	0	
690	3	320	689	0	682	outbound_asn	679	SENDER	PARTNER2	outbound_asn_in		xml	asn		asn_xml2x12_partner2	f	1	P				utf-8	0	f	text/xml 	\N	2026-10-12 03:50:53.357991	f	f		0					0		0	0	0	
689	3	310	679	0	682	outbound_asn	679	SENDER	PARTNER2	outbound_asn_in		xml	asn			f	1	P				utf-8	0	f	text/xml 	\N	2026-10-12 03:50:53.35072	f	f		0					0		0	1192	0	
693	3	320	692	0	682	outbound_asn	681	SENDER	PARTNER3	outbound_asn_in		xml	asn		asn_xml2x12_noSSCC	f	1	P				utf-8	0	f	text/xml 	\N	2026-10-12 03:50:53.425977	f	f		0					0		0	0	0	
692	3	310	681	0	682	outbound_asn	681	SENDER	PARTNER3	outbound_asn_in		xml	asn			f	1	P				utf-8	0	f	text/xml 	\N	2026-10-12 03:50:53.417827	f	f		0					0		0	3396	0	
685	3	330	684	695	682	outbound_asn	685	SENDER	PARTNER1	outbound_asn_in		x12	856004010		asn_xml2x12_default	t	1	P	71			us-ascii	0	f	application/X12	\N	2026-10-12 03:50:53.150154	f	f		0	x12				0		0	4056	0	
688	3	330	687	696	682	outbound_asn	688	SENDER	PARTNER2	outbound_asn_in		x12	856004010		asn_xml2x12_partner2	t	1	P	72			us-ascii	0	f	application/X12	\N	2026-10-12 03:50:53.292262	f	f		0	x12				0		0	1603	0	
691	3	330	690	696	682	outbound_asn	691	SENDER	PARTNER2	outbound_asn_in		x12	856004010		asn_xml2x12_partner2	t	1	P	73			us-ascii	0	f	application/X12	\N	2026-10-12 03:50:53.3699	f	f		0	x12				0		0	430	0	
696	3	400	0	0	671	outbound_asn	696	SENDER	PARTNER2	outbound_asn_in		x12	856004010			t	2	P	8			us-ascii	0	f	application/X12	\N	2026-10-12 03:50:53.53276	f	f		0	x12				0		0	2215	0	
697	3	400	0	0	671	outbound_asn	697	SENDER	PARTNER3	outbound_asn_in		x12	856004010			t	1	P	9			us-ascii	0	f	application/X12	\N	2026-10-12 03:50:53.573212	f	f		0	x12				0		0	1219	0	
702	3	520	699	0	701	outbound_asn	/o/pg/bots/botssys/outfile/demo_work_with_partners/outbound_856/PARTNER3_pgroupA_20261012_3.x12	SENDER	PARTNER3	outbound_asn_in	outbound_asn_out_pgroupA	x12	856004010			t	1	P	9			us-ascii	0	f	application/X12	\N	2026-10-12 03:50:53.681873	f	f		0	x12				0		0	0	1	
699	3	500	697	0	698	outbound_asn	697	SENDER	PARTNER3	outbound_asn_in	outbound_asn_out_pgroupA	x12	856004010			t	1	P	9			us-ascii	0	f	application/X12	\N	2026-10-12 03:50:53.630127	f	f		0	x12				0		0	0	0	
701	3	1	0	0	700	outbound_asn	outcommunicate									f	1						0	f	text/plain	\N	2026-10-12 03:50:53.673554	f	f		0					0		0	0	0	
700	3	1	0	0	698	outbound_asn	run				outbound_asn_out_pgroupA					f	1						0	f	text/plain	\N	2026-10-12 03:50:53.658811	f	f		0					0		0	0	0	
698	3	1	0	0	670	outbound_asn	routepart									f	1						0	f	text/plain	\N	2026-10-12 03:50:53.618956	f	f		0					0		0	0	0	
695	3	400	0	0	671	outbound_asn	695	SENDER	PARTNER1	outbound_asn_in		x12	856004010			t	1	P	7			us-ascii	0	f	application/X12	\N	2026-10-12 03:50:53.496782	f	f		0	x12				0		0	4238	0	
707	3	520	704	0	706	outbound_asn	/o/pg/bots/botssys/outfile/demo_work_with_partners/outbound_856/PARTNER2_20261012_3.x12	SENDER	PARTNER2	outbound_asn_in	outbound_asn_out_partner2	x12	856004010			t	2	P	8			us-ascii	0	f	application/X12	\N	2026-10-12 03:50:53.771714	f	f		0	x12				0		0	0	1	
704	3	500	696	0	703	outbound_asn	696	SENDER	PARTNER2	outbound_asn_in	outbound_asn_out_partner2	x12	856004010			t	2	P	8			us-ascii	0	f	application/X12	\N	2026-10-12 03:50:53.729765	f	f		0	x12				0		0	0	0	
706	3	1	0	0	705	outbound_asn	outcommunicate									f	1						0	f	text/plain	\N	2026-10-12 03:50:53.764169	f	f		0					0		0	0	0	
705	3	1	0	0	703	outbound_asn	run				outbound_asn_out_partner2					f	1						0	f	text/plain	\N	2026-10-12 03:50:53.751693	f	f		0					0		0	0	0	
703	3	1	0	0	670	outbound_asn	routepart									f	1						0	f	text/plain	\N	2026-10-12 03:50:53.72388	f	f		0					0		0	0	0	
711	3	1	0	0	710	outbound_asn	outcommunicate									f	1						0	f	text/plain	\N	2026-10-12 03:50:53.843585	f	f		0					0		0	0	0	
714	3	1	0	0	713	outbound_desadv	routepart									f	1						0	f	text/plain	\N	2026-10-12 03:50:53.909399	f	f		0					0		0	0	0	
712	3	520	709	0	711	outbound_asn	/o/pg/bots/botssys/outfile/demo_work_with_partners/outbound_856/PARTNER1_20261012_3.x12	SENDER	PARTNER1	outbound_asn_in	outbound_asn_out	x12	856004010			t	1	P	7			us-ascii	0	f	application/X12	\N	2026-10-12 03:50:53.848521	f	f		0	x12				0		0	0	1	
709	3	500	695	0	708	outbound_asn	695	SENDER	PARTNER1	outbound_asn_in	outbound_asn_out	x12	856004010			t	1	P	7			us-ascii	0	f	application/X12	\N	2026-10-12 03:50:53.815687	f	f		0	x12				0		0	0	0	
710	3	1	0	0	708	outbound_asn	run				outbound_asn_out					f	1						0	f	text/plain	\N	2026-10-12 03:50:53.831577	f	f		0					0		0	0	0	
708	3	1	0	0	670	outbound_asn	routepart									f	1						0	f	text/plain	\N	2026-10-12 03:50:53.810641	f	f		0					0		0	0	0	
718	3	220	717	0	716	outbound_desadv	718			outbound_desadv_in		xml	desadv			f	1						0	f	text/plain	\N	2026-10-12 03:50:53.94654	f	f		0					0		0	1320	0	
717	3	200	0	0	716	outbound_desadv	/o/pg/bots/botssys/infile/edifact_xml/xml/desadv1923.xml			outbound_desadv_in						f	1						0	f	text/plain	\N	2026-10-12 03:50:53.940487	f	f		0					0		0	0	0	
716	3	1	0	0	715	outbound_desadv	incommunicate									f	1						0	f	text/plain	\N	2026-10-12 03:50:53.929091	f	f		0					0		0	0	0	
715	3	1	0	0	714	outbound_desadv	run			outbound_desadv_in						f	1						0	f	text/plain	\N	2026-10-12 03:50:53.917	f	f		0					0		0	0	0	
713	3	1	0	0	549	outbound_desadv	router									f	1						0	f	text/plain	\N	2026-10-12 03:50:53.895215	f	f		0					0		0	0	0	
719	3	200	0	0	716	outbound_desadv	/o/pg/bots/botssys/infile/edifact_xml/xml/desadvfull01.xml			outbound_desadv_in						f	1						0	f	text/plain	\N	2026-10-12 03:50:53.972786	f	f		0					0		0	0	0	
721	3	200	0	0	716	outbound_desadv	/o/pg/bots/botssys/infile/edifact_xml/xml/desadvtest01.xml			outbound_desadv_in						f	1						0	f	text/plain	\N	2026-10-12 03:50:53.998711	f	f		0					0		0	0	0	
723	3	200	0	0	716	outbound_desadv	/o/pg/bots/botssys/infile/edifact_xml/xml/desadvtest5-1.xml			outbound_desadv_in						f	1						0	f	text/plain	\N	2026-10-12 03:50:54.024325	f	f		0					0		0	0	0	
733	3	320	732	0	731	outbound_desadv	718	5555555555555	1111111111111	outbound_desadv_in		xml	desadv		desadv_xml2edifact	f	1					utf-8	0	f	text/xml 	\N	2026-10-12 03:50:54.223919	f	f		0					0		0	0	0	
725	3	200	0	0	716	outbound_desadv	/o/pg/bots/botssys/infile/edifact_xml/xml/desadvtest5-2.xml			outbound_desadv_in						f	1						0	f	text/plain	\N	2026-10-12 03:50:54.049553	f	f		0					0		0	0	0	
732	3	310	718	0	731	outbound_desadv	718	5555555555555	1111111111111	outbound_desadv_in		xml	desadv			f	1					utf-8	0	f	text/xml 	\N	2026-10-12 03:50:54.165169	f	f		0					0		0	1320	0	
727	3	200	0	0	716	outbound_desadv	/o/pg/bots/botssys/infile/edifact_xml/xml/desadvtest6-1.xml			outbound_desadv_in						f	1						0	f	text/plain	\N	2026-10-12 03:50:54.089202	f	f		0					0		0	0	0	
729	3	200	0	0	716	outbound_desadv	/o/pg/bots/botssys/infile/edifact_xml/xml/desadvtest6-2.xml			outbound_desadv_in						f	1						0	f	text/plain	\N	2026-10-12 03:50:54.121764	f	f		0					0		0	0	0	
739	3	320	738	0	731	outbound_desadv	722	SENDER	RECEIVER	outbound_desadv_in		xml	desadv		desadv_xml2edifact	f	1					utf-8	0	f	text/xml 	\N	2026-10-12 03:50:54.430774	f	f		0					0		0	0	0	
741	3	310	724	0	731	outbound_desadv	724	5555555555555	1111111111111	outbound_desadv_in		xml	desadv			f	1					utf-8	0	f	text/xml 	\N	2026-10-12 03:50:54.507915	f	f		0					0		0	1503	0	
745	3	320	744	0	731	outbound_desadv	726	5555555555555	2222222222222	outbound_desadv_in		xml	desadv		desadv_xml2edifact	f	1					utf-8	0	f	text/xml 	\N	2026-10-12 03:50:54.609961	f	f		0					0		0	0	0	
731	3	1	0	0	714	outbound_desadv	translate									f	1						0	f	text/plain	\N	2026-10-12 03:50:54.157659	f	f		0					0		0	0	0	
738	3	310	722	0	731	outbound_desadv	722	SENDER	RECEIVER	outbound_desadv_in		xml	desadv			f	1					utf-8	0	f	text/xml 	\N	2026-10-12 03:50:54.424004	f	f		0					0		0	1571	0	
722	3	220	721	0	716	outbound_desadv	722			outbound_desadv_in		xml	desadv			f	1						0	f	text/plain	\N	2026-10-12 03:50:54.005578	f	f		0					0		0	1571	0	
736	3	320	735	0	731	outbound_desadv	720	5555555555555	1111111111111	outbound_desadv_in		xml	desadv		desadv_xml2edifact	f	1					utf-8	0	f	text/xml 	\N	2026-10-12 03:50:54.318149	f	f		0					0		0	0	0	
735	3	310	720	0	731	outbound_desadv	720	5555555555555	1111111111111	outbound_desadv_in		xml	desadv			f	1					utf-8	0	f	text/xml 	\N	2026-10-12 03:50:54.307404	f	f		0					0		0	11810	0	
720	3	220	719	0	716	outbound_desadv	720			outbound_desadv_in		xml	desadv			f	1						0	f	text/plain	\N	2026-10-12 03:50:53.977994	f	f		0					0		0	11810	0	
724	3	220	723	0	716	outbound_desadv	724			outbound_desadv_in		xml	desadv			f	1						0	f	text/plain	\N	2026-10-12 03:50:54.031104	f	f		0					0		0	1503	0	
747	3	310	728	0	731	outbound_desadv	728	6666666666666	1111111111111	outbound_desadv_in		xml	desadv			f	1					utf-8	0	f	text/xml 	\N	2026-10-12 03:50:54.682558	f	f		0					0		0	1503	0	
742	3	320	741	0	731	outbound_desadv	724	5555555555555	1111111111111	outbound_desadv_in		xml	desadv		desadv_xml2edifact	f	1					utf-8	0	f	text/xml 	\N	2026-10-12 03:50:54.529887	f	f		0					0		0	0	0	
744	3	310	726	0	731	outbound_desadv	726	5555555555555	2222222222222	outbound_desadv_in		xml	desadv			f	1					utf-8	0	f	text/xml 	\N	2026-10-12 03:50:54.603303	f	f		0					0		0	1503	0	
726	3	220	725	0	716	outbound_desadv	726			outbound_desadv_in		xml	desadv			f	1						0	f	text/plain	\N	2026-10-12 03:50:54.05586	f	f		0					0		0	1503	0	
748	3	320	747	0	731	outbound_desadv	728	6666666666666	1111111111111	outbound_desadv_in		xml	desadv		desadv_xml2edifact	f	1					utf-8	0	f	text/xml 	\N	2026-10-12 03:50:54.689682	f	f		0					0		0	0	0	
728	3	220	727	0	716	outbound_desadv	728			outbound_desadv_in		xml	desadv			f	1						0	f	text/plain	\N	2026-10-12 03:50:54.094412	f	f		0					0		0	1503	0	
750	3	310	730	0	731	outbound_desadv	730	6666666666666	2222222222222	outbound_desadv_in		xml	desadv			f	1					utf-8	0	f	text/xml 	\N	2026-10-12 03:50:54.754815	f	f		0					0		0	1503	0	
751	3	320	750	0	731	outbound_desadv	730	6666666666666	2222222222222	outbound_desadv_in		xml	desadv		desadv_xml2edifact	f	1					utf-8	0	f	text/xml 	\N	2026-10-12 03:50:54.762004	f	f		0					0		0	0	0	
730	3	220	729	0	716	outbound_desadv	730			outbound_desadv_in		xml	desadv			f	1						0	f	text/plain	\N	2026-10-12 03:50:54.128574	f	f		0					0		0	1503	0	
734	3	330	733	753	731	outbound_desadv	734	5555555555555	1111111111111	outbound_desadv_in		edifact	DESADVD96AUNEAN005		desadv_xml2edifact	t	1		75			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:54.246901	f	f		0	edifact				0		0	366	0	
737	3	330	736	753	731	outbound_desadv	737	5555555555555	1111111111111	outbound_desadv_in		edifact	DESADVD96AUNEAN005		desadv_xml2edifact	t	1		76			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:54.327805	f	f		0	edifact				0		0	2793	0	
743	3	330	742	753	731	outbound_desadv	743	5555555555555	1111111111111	outbound_desadv_in		edifact	DESADVD96AUNEAN005		desadv_xml2edifact	t	1		78			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:54.548556	f	f		0	edifact				0		0	495	0	
746	3	330	745	754	731	outbound_desadv	746	5555555555555	2222222222222	outbound_desadv_in		edifact	DESADVD96AUNEAN005		desadv_xml2edifact	t	1		79			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:54.625213	f	f		0	edifact				0		0	495	0	
749	3	330	748	755	731	outbound_desadv	749	6666666666666	1111111111111	outbound_desadv_in		edifact	DESADVD96AUNEAN005		desadv_xml2edifact	t	1		80			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:54.705816	f	f		0	edifact				0		0	495	0	
740	3	330	739	757	731	outbound_desadv	740	SENDER	RECEIVER	outbound_desadv_in		edifact	DESADVD96AUNEAN005		desadv_xml2edifact	t	1		77			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:54.442505	f	f		0	edifact				0		0	495	0	
752	3	330	751	756	731	outbound_desadv	752	6666666666666	2222222222222	outbound_desadv_in		edifact	DESADVD96AUNEAN005		desadv_xml2edifact	t	1		81			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:54.776714	f	f		0	edifact				0		0	495	0	
768	3	520	761	0	764	outbound_desadv	/o/pg/bots/botssys/outfile/edifact_xml/edifact/desadv14.edi	6666666666666	2222222222222	outbound_desadv_in	outbound_desadv_out	edifact	DESADVD96AUNEAN005			t	1		10			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:55.195989	f	f		0	edifact				0		0	0	1	
753	3	400	0	0	714	outbound_desadv	753	5555555555555	1111111111111	outbound_desadv_in		edifact	DESADVD96AUNEAN005			t	3		9			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:54.842594	f	f		0	edifact				0		0	3736	0	
761	3	500	756	0	714	outbound_desadv	756	6666666666666	2222222222222	outbound_desadv_in	outbound_desadv_out	edifact	DESADVD96AUNEAN005			t	1		10			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:55.073806	f	f		0	edifact				0		0	0	0	
754	3	400	0	0	714	outbound_desadv	754	5555555555555	2222222222222	outbound_desadv_in		edifact	DESADVD96AUNEAN005			t	1		10			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:54.894327	f	f		0	edifact				0		0	579	0	
755	3	400	0	0	714	outbound_desadv	755	6666666666666	1111111111111	outbound_desadv_in		edifact	DESADVD96AUNEAN005			t	1		9			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:54.923877	f	f		0	edifact				0		0	577	0	
756	3	400	0	0	714	outbound_desadv	756	6666666666666	2222222222222	outbound_desadv_in		edifact	DESADVD96AUNEAN005			t	1		10			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:54.965886	f	f		0	edifact				0		0	579	0	
775	3	220	774	0	773	outbound_invoice	775			outbound_invoice_in		xml	invoice			f	1						0	f	text/plain	\N	2026-10-12 03:50:55.339151	f	f		0					0		0	5539	0	
757	3	400	0	0	714	outbound_desadv	757	SENDER	RECEIVER	outbound_desadv_in		edifact	DESADVD96AUNEAN005			t	1		5			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:54.994792	f	f		0	edifact				0		0	565	0	
774	3	200	0	0	773	outbound_invoice	/o/pg/bots/botssys/infile/edifact_xml/xml/invoicfull01.xml			outbound_invoice_in						f	1						0	f	text/plain	\N	2026-10-12 03:50:55.328772	f	f		0					0		0	0	0	
765	3	520	758	0	764	outbound_desadv	/o/pg/bots/botssys/outfile/edifact_xml/edifact/desadv11.edi	5555555555555	1111111111111	outbound_desadv_in	outbound_desadv_out	edifact	DESADVD96AUNEAN005			t	3		9			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:55.120578	f	f		0	edifact				0		0	0	1	
758	3	500	753	0	714	outbound_desadv	753	5555555555555	1111111111111	outbound_desadv_in	outbound_desadv_out	edifact	DESADVD96AUNEAN005			t	3		9			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:55.031122	f	f		0	edifact				0		0	0	0	
766	3	520	759	0	764	outbound_desadv	/o/pg/bots/botssys/outfile/edifact_xml/edifact/desadv12.edi	5555555555555	2222222222222	outbound_desadv_in	outbound_desadv_out	edifact	DESADVD96AUNEAN005			t	1		10			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:55.146545	f	f		0	edifact				0		0	0	1	
759	3	500	754	0	714	outbound_desadv	754	5555555555555	2222222222222	outbound_desadv_in	outbound_desadv_out	edifact	DESADVD96AUNEAN005			t	1		10			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:55.046847	f	f		0	edifact				0		0	0	0	
767	3	520	760	0	764	outbound_desadv	/o/pg/bots/botssys/outfile/edifact_xml/edifact/desadv13.edi	6666666666666	1111111111111	outbound_desadv_in	outbound_desadv_out	edifact	DESADVD96AUNEAN005			t	1		9			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:55.174065	f	f		0	edifact				0		0	0	1	
760	3	500	755	0	714	outbound_desadv	755	6666666666666	1111111111111	outbound_desadv_in	outbound_desadv_out	edifact	DESADVD96AUNEAN005			t	1		9			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:55.059877	f	f		0	edifact				0		0	0	0	
769	3	520	762	0	764	outbound_desadv	/o/pg/bots/botssys/outfile/edifact_xml/edifact/desadv15.edi	SENDER	RECEIVER	outbound_desadv_in	outbound_desadv_out	edifact	DESADVD96AUNEAN005			t	1		5			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:55.235398	f	f		0	edifact				0		0	0	1	
762	3	500	757	0	714	outbound_desadv	757	SENDER	RECEIVER	outbound_desadv_in	outbound_desadv_out	edifact	DESADVD96AUNEAN005			t	1		5			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:55.086763	f	f		0	edifact				0		0	0	0	
764	3	1	0	0	763	outbound_desadv	outcommunicate									f	1						0	f	text/plain	\N	2026-10-12 03:50:55.115124	f	f		0					0		0	0	0	
763	3	1	0	0	714	outbound_desadv	run				outbound_desadv_out					f	1						0	f	text/plain	\N	2026-10-12 03:50:55.100723	f	f		0					0		0	0	0	
771	3	1	0	0	770	outbound_invoice	routepart									f	1						0	f	text/plain	\N	2026-10-12 03:50:55.285238	f	f		0					0		0	0	0	
770	3	1	0	0	549	outbound_invoice	router									f	1						0	f	text/plain	\N	2026-10-12 03:50:55.278653	f	f		0					0		0	0	0	
776	3	200	0	0	773	outbound_invoice	/o/pg/bots/botssys/infile/edifact_xml/xml/invoictest01.xml			outbound_invoice_in						f	1						0	f	text/plain	\N	2026-10-12 03:50:55.3624	f	f		0					0		0	0	0	
778	3	200	0	0	773	outbound_invoice	/o/pg/bots/botssys/infile/edifact_xml/xml/invoictest5-1.xml			outbound_invoice_in						f	1						0	f	text/plain	\N	2026-10-12 03:50:55.391896	f	f		0					0		0	0	0	
780	3	200	0	0	773	outbound_invoice	/o/pg/bots/botssys/infile/edifact_xml/xml/invoictest5-2.xml			outbound_invoice_in						f	1						0	f	text/plain	\N	2026-10-12 03:50:55.417601	f	f		0					0		0	0	0	
782	3	200	0	0	773	outbound_invoice	/o/pg/bots/botssys/infile/edifact_xml/xml/invoictest6-1.xml			outbound_invoice_in						f	1						0	f	text/plain	\N	2026-10-12 03:50:55.446852	f	f		0					0		0	0	0	
773	3	1	0	0	772	outbound_invoice	incommunicate									f	1						0	f	text/plain	\N	2026-10-12 03:50:55.306016	f	f		0					0		0	0	0	
772	3	1	0	0	771	outbound_invoice	run			outbound_invoice_in						f	1						0	f	text/plain	\N	2026-10-12 03:50:55.292482	f	f		0					0		0	0	0	
794	3	320	793	0	786	outbound_invoice	779	5555555555555	1111111111111	outbound_invoice_in		xml	invoice		invoice_xml2edifact	f	1					utf-8	0	f	text/xml 	\N	2026-10-12 03:50:55.726929	f	f		0					0		0	0	0	
784	3	200	0	0	773	outbound_invoice	/o/pg/bots/botssys/infile/edifact_xml/xml/invoictest6-2.xml			outbound_invoice_in						f	1						0	f	text/plain	\N	2026-10-12 03:50:55.478951	f	f		0					0		0	0	0	
803	3	320	802	0	786	outbound_invoice	785	6666666666666	2222222222222	outbound_invoice_in		xml	invoice		invoice_xml2edifact	f	1					utf-8	0	f	text/xml 	\N	2026-10-12 03:50:56.000256	f	f		0					0		0	0	0	
795	3	330	794	805	786	outbound_invoice	795	5555555555555	1111111111111	outbound_invoice_in		edifact	INVOICD96AUNEAN008		invoice_xml2edifact	t	1		84			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:55.737409	f	f		0	edifact				0		0	744	0	
793	3	310	779	0	786	outbound_invoice	779	5555555555555	1111111111111	outbound_invoice_in		xml	invoice			f	1					utf-8	0	f	text/xml 	\N	2026-10-12 03:50:55.71961	f	f		0					0		0	2208	0	
779	3	220	778	0	773	outbound_invoice	779			outbound_invoice_in		xml	invoice			f	1						0	f	text/plain	\N	2026-10-12 03:50:55.398892	f	f		0					0		0	2208	0	
788	3	320	787	0	786	outbound_invoice	775	5555555555555	1111111111111	outbound_invoice_in		xml	invoice		invoice_xml2edifact	f	1					utf-8	0	f	text/xml 	\N	2026-10-12 03:50:55.553421	f	f		0					0		0	0	0	
787	3	310	775	0	786	outbound_invoice	775	5555555555555	1111111111111	outbound_invoice_in		xml	invoice			f	1					utf-8	0	f	text/xml 	\N	2026-10-12 03:50:55.536606	f	f		0					0		0	5539	0	
791	3	320	790	0	786	outbound_invoice	777	SENDER	RECEIVER	outbound_invoice_in		xml	invoice		invoice_xml2edifact	f	1					utf-8	0	f	text/xml 	\N	2026-10-12 03:50:55.654081	f	f		0					0		0	0	0	
790	3	310	777	0	786	outbound_invoice	777	SENDER	RECEIVER	outbound_invoice_in		xml	invoice			f	1					utf-8	0	f	text/xml 	\N	2026-10-12 03:50:55.647023	f	f		0					0		0	2196	0	
777	3	220	776	0	773	outbound_invoice	777			outbound_invoice_in		xml	invoice			f	1						0	f	text/plain	\N	2026-10-12 03:50:55.36752	f	f		0					0		0	2196	0	
800	3	320	799	0	786	outbound_invoice	783	6666666666666	1111111111111	outbound_invoice_in		xml	invoice		invoice_xml2edifact	f	1					utf-8	0	f	text/xml 	\N	2026-10-12 03:50:55.927124	f	f		0					0		0	0	0	
799	3	310	783	0	786	outbound_invoice	783	6666666666666	1111111111111	outbound_invoice_in		xml	invoice			f	1					utf-8	0	f	text/xml 	\N	2026-10-12 03:50:55.914885	f	f		0					0		0	2208	0	
797	3	320	796	0	786	outbound_invoice	781	5555555555555	2222222222222	outbound_invoice_in		xml	invoice		invoice_xml2edifact	f	1					utf-8	0	f	text/xml 	\N	2026-10-12 03:50:55.815825	f	f		0					0		0	0	0	
796	3	310	781	0	786	outbound_invoice	781	5555555555555	2222222222222	outbound_invoice_in		xml	invoice			f	1					utf-8	0	f	text/xml 	\N	2026-10-12 03:50:55.805404	f	f		0					0		0	2208	0	
781	3	220	780	0	773	outbound_invoice	781			outbound_invoice_in		xml	invoice			f	1						0	f	text/plain	\N	2026-10-12 03:50:55.429255	f	f		0					0		0	2208	0	
802	3	310	785	0	786	outbound_invoice	785	6666666666666	2222222222222	outbound_invoice_in		xml	invoice			f	1					utf-8	0	f	text/xml 	\N	2026-10-12 03:50:55.993072	f	f		0					0		0	2208	0	
785	3	220	784	0	773	outbound_invoice	785			outbound_invoice_in		xml	invoice			f	1						0	f	text/plain	\N	2026-10-12 03:50:55.484403	f	f		0					0		0	2208	0	
783	3	220	782	0	773	outbound_invoice	783			outbound_invoice_in		xml	invoice			f	1						0	f	text/plain	\N	2026-10-12 03:50:55.451789	f	f		0					0		0	2208	0	
786	3	1	0	0	771	outbound_invoice	translate									f	1						0	f	text/plain	\N	2026-10-12 03:50:55.521858	f	f		0					0		0	0	0	
789	3	330	788	805	786	outbound_invoice	789	5555555555555	1111111111111	outbound_invoice_in		edifact	INVOICD96AUNEAN008		invoice_xml2edifact	t	1		82			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:55.568375	f	f		0	edifact				0		0	1579	0	
798	3	330	797	806	786	outbound_invoice	798	5555555555555	2222222222222	outbound_invoice_in		edifact	INVOICD96AUNEAN008		invoice_xml2edifact	t	1		85			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:55.828086	f	f		0	edifact				0		0	744	0	
801	3	330	800	807	786	outbound_invoice	801	6666666666666	1111111111111	outbound_invoice_in		edifact	INVOICD96AUNEAN008		invoice_xml2edifact	t	1		86			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:55.937958	f	f		0	edifact				0		0	744	0	
804	3	330	803	808	786	outbound_invoice	804	6666666666666	2222222222222	outbound_invoice_in		edifact	INVOICD96AUNEAN008		invoice_xml2edifact	t	1		87			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:56.017928	f	f		0	edifact				0		0	744	0	
792	3	330	791	809	786	outbound_invoice	792	SENDER	RECEIVER	outbound_invoice_in		edifact	INVOICD96AUNEAN008		invoice_xml2edifact	t	1		83			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:55.664099	f	f		0	edifact				0		0	744	0	
805	3	400	0	0	771	outbound_invoice	805	5555555555555	1111111111111	outbound_invoice_in		edifact	INVOICD96AUNEAN008			t	2		11			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:56.078008	f	f		0	edifact				0		0	2407	0	
806	3	400	0	0	771	outbound_invoice	806	5555555555555	2222222222222	outbound_invoice_in		edifact	INVOICD96AUNEAN008			t	1		12			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:56.113291	f	f		0	edifact				0		0	828	0	
807	3	400	0	0	771	outbound_invoice	807	6666666666666	1111111111111	outbound_invoice_in		edifact	INVOICD96AUNEAN008			t	1		11			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:56.145245	f	f		0	edifact				0		0	828	0	
808	3	400	0	0	771	outbound_invoice	808	6666666666666	2222222222222	outbound_invoice_in		edifact	INVOICD96AUNEAN008			t	1		12			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:56.175551	f	f		0	edifact				0		0	828	0	
809	3	400	0	0	771	outbound_invoice	809	SENDER	RECEIVER	outbound_invoice_in		edifact	INVOICD96AUNEAN008			t	1		6			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:56.207841	f	f		0	edifact				0		0	814	0	
810	3	500	805	0	771	outbound_invoice	805	5555555555555	1111111111111	outbound_invoice_in	outbound_invoice_out	edifact	INVOICD96AUNEAN008			t	2		11			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:56.240849	f	f		0	edifact				0		0	0	0	
817	3	520	810	0	816	outbound_invoice	/o/pg/bots/botssys/outfile/edifact_xml/edifact/invoic11.edi	5555555555555	1111111111111	outbound_invoice_in	outbound_invoice_out	edifact	INVOICD96AUNEAN008			t	2		11			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:56.333493	f	f		0	edifact				0		0	0	1	
818	3	520	811	0	816	outbound_invoice	/o/pg/bots/botssys/outfile/edifact_xml/edifact/invoic12.edi	5555555555555	2222222222222	outbound_invoice_in	outbound_invoice_out	edifact	INVOICD96AUNEAN008			t	1		12			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:56.380545	f	f		0	edifact				0		0	0	1	
811	3	500	806	0	771	outbound_invoice	806	5555555555555	2222222222222	outbound_invoice_in	outbound_invoice_out	edifact	INVOICD96AUNEAN008			t	1		12			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:56.255043	f	f		0	edifact				0		0	0	0	
819	3	520	812	0	816	outbound_invoice	/o/pg/bots/botssys/outfile/edifact_xml/edifact/invoic13.edi	6666666666666	1111111111111	outbound_invoice_in	outbound_invoice_out	edifact	INVOICD96AUNEAN008			t	1		11			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:56.409419	f	f		0	edifact				0		0	0	1	
812	3	500	807	0	771	outbound_invoice	807	6666666666666	1111111111111	outbound_invoice_in	outbound_invoice_out	edifact	INVOICD96AUNEAN008			t	1		11			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:56.270079	f	f		0	edifact				0		0	0	0	
820	3	520	813	0	816	outbound_invoice	/o/pg/bots/botssys/outfile/edifact_xml/edifact/invoic14.edi	6666666666666	2222222222222	outbound_invoice_in	outbound_invoice_out	edifact	INVOICD96AUNEAN008			t	1		12			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:56.433239	f	f		0	edifact				0		0	0	1	
813	3	500	808	0	771	outbound_invoice	808	6666666666666	2222222222222	outbound_invoice_in	outbound_invoice_out	edifact	INVOICD96AUNEAN008			t	1		12			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:56.284738	f	f		0	edifact				0		0	0	0	
821	3	520	814	0	816	outbound_invoice	/o/pg/bots/botssys/outfile/edifact_xml/edifact/invoic15.edi	SENDER	RECEIVER	outbound_invoice_in	outbound_invoice_out	edifact	INVOICD96AUNEAN008			t	1		6			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:56.458083	f	f		0	edifact				0		0	0	1	
814	3	500	809	0	771	outbound_invoice	809	SENDER	RECEIVER	outbound_invoice_in	outbound_invoice_out	edifact	INVOICD96AUNEAN008			t	1		6			UNOC	0	f	application/EDIFACT	\N	2026-10-12 03:50:56.298786	f	f		0	edifact				0		0	0	0	
816	3	1	0	0	815	outbound_invoice	outcommunicate									f	1						0	f	text/plain	\N	2026-10-12 03:50:56.326724	f	f		0					0		0	0	0	
815	3	1	0	0	771	outbound_invoice	run				outbound_invoice_out					f	1						0	f	text/plain	\N	2026-10-12 03:50:56.312977	f	f		0					0		0	0	0	
\.


--
-- Data for Name: translate; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.translate (id, active, fromeditype, frommessagetype, alt, frompartner_id, topartner_id, tscript, toeditype, tomessagetype, "desc", rsrv1, rsrv2) FROM stdin;
1	t	edifact	ORDERSD96AUNEAN008		\N	\N	orders_edifact2xml	xml	orders		\N	\N
2	t	xml	desadv		\N	\N	desadv_xml2edifact	edifact	DESADVD96AUNEAN005		\N	\N
3	t	xml	invoice		\N	\N	invoice_xml2edifact	edifact	INVOICD96AUNEAN008		\N	\N
4	t	x12	856004010		\N	\N	inn2out	x12	856004010		\N	\N
5	t	xml	asn		\N	\N	asn_xml2x12_default	x12	856004010		\N	\N
6	t	xml	asn		\N	PARTNER2	asn_xml2x12_partner2	x12	856004010		\N	\N
7	t	xml	asn		\N	PGROUP_A	asn_xml2x12_noSSCC	x12	856004010		\N	\N
\.


--
-- Data for Name: uniek; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.uniek (domein, nummer) FROM stdin;
audit_counter	3
isacounter_FROMPARTNER2	3
demo_partner_conversion_out	3
inbound_orders_out	18
myfirstroute_out	15
isacounter_SENDER	9
outbound_asn_out_pgroupA	3
outbound_asn_out_partner2	3
outbound_asn_out	3
outbound_desadv_out	15
messagecounter	87
unbcounter_5555555555555	12
unbcounter_6666666666666	12
unbcounter_SENDER	6
outbound_invoice_out	15
bots_cleanup_day	20261012
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, true);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, true);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 63, true);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, true);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 3, true);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 15, true);


--
-- Name: ccode_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.ccode_id_seq', 2, true);


--
-- Name: chanpar_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.chanpar_id_seq', 1, false);


--
-- Name: confirmrule_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.confirmrule_id_seq', 1, false);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 21, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 4, true);


--
-- Name: partnergroup_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.partnergroup_id_seq', 2, true);


--
-- Name: routes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.routes_id_seq', 9, true);


--
-- Name: ta_idta_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.ta_idta_seq', 821, true);


--
-- Name: translate_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.translate_id_seq', 7, true);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_key UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_key UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_key UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_key UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: ccode ccode_ccodeid_id_leftcode_rightcode_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ccode
    ADD CONSTRAINT ccode_ccodeid_id_leftcode_rightcode_key UNIQUE (ccodeid_id, leftcode, rightcode);


--
-- Name: ccode ccode_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ccode
    ADD CONSTRAINT ccode_pkey PRIMARY KEY (id);


--
-- Name: ccodetrigger ccodetrigger_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ccodetrigger
    ADD CONSTRAINT ccodetrigger_pkey PRIMARY KEY (ccodeid);


--
-- Name: channel channel_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.channel
    ADD CONSTRAINT channel_pkey PRIMARY KEY (idchannel);


--
-- Name: chanpar chanpar_idpartner_id_idchannel_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chanpar
    ADD CONSTRAINT chanpar_idpartner_id_idchannel_id_key UNIQUE (idpartner_id, idchannel_id);


--
-- Name: chanpar chanpar_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chanpar
    ADD CONSTRAINT chanpar_pkey PRIMARY KEY (id);


--
-- Name: confirmrule confirmrule_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.confirmrule
    ADD CONSTRAINT confirmrule_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_45f3b1d93ec8c61c_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_45f3b1d93ec8c61c_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: filereport filereport_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.filereport
    ADD CONSTRAINT filereport_pkey PRIMARY KEY (idta);


--
-- Name: mutex mutex_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mutex
    ADD CONSTRAINT mutex_pkey PRIMARY KEY (mutexk);


--
-- Name: partner partner_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.partner
    ADD CONSTRAINT partner_pkey PRIMARY KEY (idpartner);


--
-- Name: partnergroup partnergroup_from_partner_id_to_partner_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.partnergroup
    ADD CONSTRAINT partnergroup_from_partner_id_to_partner_id_key UNIQUE (from_partner_id, to_partner_id);


--
-- Name: partnergroup partnergroup_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.partnergroup
    ADD CONSTRAINT partnergroup_pkey PRIMARY KEY (id);


--
-- Name: persist persist_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.persist
    ADD CONSTRAINT persist_pkey PRIMARY KEY (domein, botskey);


--
-- Name: report report_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.report
    ADD CONSTRAINT report_pkey PRIMARY KEY (idta);


--
-- Name: routes routes_idroute_seq_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.routes
    ADD CONSTRAINT routes_idroute_seq_key UNIQUE (idroute, seq);


--
-- Name: routes routes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.routes
    ADD CONSTRAINT routes_pkey PRIMARY KEY (id);


--
-- Name: ta ta_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ta
    ADD CONSTRAINT ta_pkey PRIMARY KEY (idta);


--
-- Name: translate translate_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.translate
    ADD CONSTRAINT translate_pkey PRIMARY KEY (id);


--
-- Name: uniek uniek_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.uniek
    ADD CONSTRAINT uniek_pkey PRIMARY KEY (domein);


--
-- Name: auth_group_name_253ae2a6331666e8_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_name_253ae2a6331666e8_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_0e939a4f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_permissions_0e939a4f ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_8373b171; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_permissions_8373b171 ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_417f1b1c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_permission_417f1b1c ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_0e939a4f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_groups_0e939a4f ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_e8701ad4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_groups_e8701ad4 ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_8373b171; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_user_permissions_8373b171 ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_e8701ad4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_user_permissions_e8701ad4 ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_51b3b110094b8aae_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_username_51b3b110094b8aae_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: ccode_ccodeid_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ccode_ccodeid_id ON public.ccode USING btree (ccodeid_id);


--
-- Name: ccode_ccodeid_id_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ccode_ccodeid_id_like ON public.ccode USING btree (ccodeid_id varchar_pattern_ops);


--
-- Name: ccode_leftcode; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ccode_leftcode ON public.ccode USING btree (leftcode);


--
-- Name: ccode_leftcode_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ccode_leftcode_like ON public.ccode USING btree (leftcode varchar_pattern_ops);


--
-- Name: ccode_rightcode; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ccode_rightcode ON public.ccode USING btree (rightcode);


--
-- Name: ccode_rightcode_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ccode_rightcode_like ON public.ccode USING btree (rightcode varchar_pattern_ops);


--
-- Name: ccodetrigger_ccodeid_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ccodetrigger_ccodeid_like ON public.ccodetrigger USING btree (ccodeid varchar_pattern_ops);


--
-- Name: channel_idchannel_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX channel_idchannel_like ON public.channel USING btree (idchannel varchar_pattern_ops);


--
-- Name: chanpar_idchannel_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX chanpar_idchannel_id ON public.chanpar USING btree (idchannel_id);


--
-- Name: chanpar_idchannel_id_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX chanpar_idchannel_id_like ON public.chanpar USING btree (idchannel_id varchar_pattern_ops);


--
-- Name: chanpar_idpartner_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX chanpar_idpartner_id ON public.chanpar USING btree (idpartner_id);


--
-- Name: chanpar_idpartner_id_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX chanpar_idpartner_id_like ON public.chanpar USING btree (idpartner_id varchar_pattern_ops);


--
-- Name: confirmrule_frompartner_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX confirmrule_frompartner_id ON public.confirmrule USING btree (frompartner_id);


--
-- Name: confirmrule_frompartner_id_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX confirmrule_frompartner_id_like ON public.confirmrule USING btree (frompartner_id varchar_pattern_ops);


--
-- Name: confirmrule_idchannel_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX confirmrule_idchannel_id ON public.confirmrule USING btree (idchannel_id);


--
-- Name: confirmrule_idchannel_id_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX confirmrule_idchannel_id_like ON public.confirmrule USING btree (idchannel_id varchar_pattern_ops);


--
-- Name: confirmrule_topartner_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX confirmrule_topartner_id ON public.confirmrule USING btree (topartner_id);


--
-- Name: confirmrule_topartner_id_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX confirmrule_topartner_id_like ON public.confirmrule USING btree (topartner_id varchar_pattern_ops);


--
-- Name: django_admin_log_417f1b1c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_admin_log_417f1b1c ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_e8701ad4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_admin_log_e8701ad4 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_de54fa62; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_session_de54fa62 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_461cfeaa630ca218_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_session_session_key_461cfeaa630ca218_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: filereport_ts; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX filereport_ts ON public.filereport USING btree (ts);


--
-- Name: partner_idpartner_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX partner_idpartner_like ON public.partner USING btree (idpartner varchar_pattern_ops);


--
-- Name: partnergroup_from_partner_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX partnergroup_from_partner_id ON public.partnergroup USING btree (from_partner_id);


--
-- Name: partnergroup_from_partner_id_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX partnergroup_from_partner_id_like ON public.partnergroup USING btree (from_partner_id varchar_pattern_ops);


--
-- Name: partnergroup_to_partner_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX partnergroup_to_partner_id ON public.partnergroup USING btree (to_partner_id);


--
-- Name: partnergroup_to_partner_id_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX partnergroup_to_partner_id_like ON public.partnergroup USING btree (to_partner_id varchar_pattern_ops);


--
-- Name: report_ts; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX report_ts ON public.report USING btree (ts);


--
-- Name: routes_fromchannel_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX routes_fromchannel_id ON public.routes USING btree (fromchannel_id);


--
-- Name: routes_fromchannel_id_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX routes_fromchannel_id_like ON public.routes USING btree (fromchannel_id varchar_pattern_ops);


--
-- Name: routes_frompartner_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX routes_frompartner_id ON public.routes USING btree (frompartner_id);


--
-- Name: routes_frompartner_id_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX routes_frompartner_id_like ON public.routes USING btree (frompartner_id varchar_pattern_ops);


--
-- Name: routes_frompartner_tochannel_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX routes_frompartner_tochannel_id ON public.routes USING btree (frompartner_tochannel_id);


--
-- Name: routes_frompartner_tochannel_id_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX routes_frompartner_tochannel_id_like ON public.routes USING btree (frompartner_tochannel_id varchar_pattern_ops);


--
-- Name: routes_idroute; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX routes_idroute ON public.routes USING btree (idroute);


--
-- Name: routes_idroute_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX routes_idroute_like ON public.routes USING btree (idroute varchar_pattern_ops);


--
-- Name: routes_tochannel_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX routes_tochannel_id ON public.routes USING btree (tochannel_id);


--
-- Name: routes_tochannel_id_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX routes_tochannel_id_like ON public.routes USING btree (tochannel_id varchar_pattern_ops);


--
-- Name: routes_topartner_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX routes_topartner_id ON public.routes USING btree (topartner_id);


--
-- Name: routes_topartner_id_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX routes_topartner_id_like ON public.routes USING btree (topartner_id varchar_pattern_ops);


--
-- Name: routes_topartner_tochannel_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX routes_topartner_tochannel_id ON public.routes USING btree (topartner_tochannel_id);


--
-- Name: routes_topartner_tochannel_id_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX routes_topartner_tochannel_id_like ON public.routes USING btree (topartner_tochannel_id varchar_pattern_ops);


--
-- Name: ta_parent; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ta_parent ON public.ta USING btree (parent);


--
-- Name: ta_reference; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ta_reference ON public.ta USING btree (reference);


--
-- Name: ta_reference_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ta_reference_like ON public.ta USING btree (reference varchar_pattern_ops);


--
-- Name: translate_frompartner_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX translate_frompartner_id ON public.translate USING btree (frompartner_id);


--
-- Name: translate_frompartner_id_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX translate_frompartner_id_like ON public.translate USING btree (frompartner_id varchar_pattern_ops);


--
-- Name: translate_topartner_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX translate_topartner_id ON public.translate USING btree (topartner_id);


--
-- Name: translate_topartner_id_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX translate_topartner_id_like ON public.translate USING btree (topartner_id varchar_pattern_ops);


--
-- Name: uniek_domein_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX uniek_domein_like ON public.uniek USING btree (domein varchar_pattern_ops);


--
-- Name: auth_permission auth_content_type_id_508cf46651277a81_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_content_type_id_508cf46651277a81_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissio_group_id_689710a9a73b7457_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_group_id_689710a9a73b7457_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user__permission_id_384b62483d7071f0_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user__permission_id_384b62483d7071f0_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_4b5ed4ffdb8fd9b0_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_4b5ed4ffdb8fd9b0_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permiss_user_id_7f0938558328534a_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permiss_user_id_7f0938558328534a_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ccode ccode_ccodeid_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ccode
    ADD CONSTRAINT ccode_ccodeid_id_fkey FOREIGN KEY (ccodeid_id) REFERENCES public.ccodetrigger(ccodeid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: chanpar chanpar_idchannel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chanpar
    ADD CONSTRAINT chanpar_idchannel_id_fkey FOREIGN KEY (idchannel_id) REFERENCES public.channel(idchannel) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: chanpar chanpar_idpartner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chanpar
    ADD CONSTRAINT chanpar_idpartner_id_fkey FOREIGN KEY (idpartner_id) REFERENCES public.partner(idpartner) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log djan_content_type_id_697914295151027a_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT djan_content_type_id_697914295151027a_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partnergroup from_partner_id_refs_idpartner_0347e6b2; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.partnergroup
    ADD CONSTRAINT from_partner_id_refs_idpartner_0347e6b2 FOREIGN KEY (from_partner_id) REFERENCES public.partner(idpartner) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: confirmrule frompartner_id_refs_idpartner_bd266b77; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.confirmrule
    ADD CONSTRAINT frompartner_id_refs_idpartner_bd266b77 FOREIGN KEY (frompartner_id) REFERENCES public.partner(idpartner) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: confirmrule idchannel_id_refs_idchannel_d1c3083e; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.confirmrule
    ADD CONSTRAINT idchannel_id_refs_idchannel_d1c3083e FOREIGN KEY (idchannel_id) REFERENCES public.channel(idchannel) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: routes routes_fromchannel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.routes
    ADD CONSTRAINT routes_fromchannel_id_fkey FOREIGN KEY (fromchannel_id) REFERENCES public.channel(idchannel) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: routes routes_frompartner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.routes
    ADD CONSTRAINT routes_frompartner_id_fkey FOREIGN KEY (frompartner_id) REFERENCES public.partner(idpartner) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: routes routes_frompartner_tochannel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.routes
    ADD CONSTRAINT routes_frompartner_tochannel_id_fkey FOREIGN KEY (frompartner_tochannel_id) REFERENCES public.partner(idpartner) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: routes routes_tochannel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.routes
    ADD CONSTRAINT routes_tochannel_id_fkey FOREIGN KEY (tochannel_id) REFERENCES public.channel(idchannel) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: routes routes_topartner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.routes
    ADD CONSTRAINT routes_topartner_id_fkey FOREIGN KEY (topartner_id) REFERENCES public.partner(idpartner) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: routes routes_topartner_tochannel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.routes
    ADD CONSTRAINT routes_topartner_tochannel_id_fkey FOREIGN KEY (topartner_tochannel_id) REFERENCES public.partner(idpartner) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partnergroup to_partner_id_refs_idpartner_0347e6b2; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.partnergroup
    ADD CONSTRAINT to_partner_id_refs_idpartner_0347e6b2 FOREIGN KEY (to_partner_id) REFERENCES public.partner(idpartner) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: confirmrule topartner_id_refs_idpartner_bd266b77; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.confirmrule
    ADD CONSTRAINT topartner_id_refs_idpartner_bd266b77 FOREIGN KEY (topartner_id) REFERENCES public.partner(idpartner) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: translate translate_frompartner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.translate
    ADD CONSTRAINT translate_frompartner_id_fkey FOREIGN KEY (frompartner_id) REFERENCES public.partner(idpartner) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: translate translate_topartner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.translate
    ADD CONSTRAINT translate_topartner_id_fkey FOREIGN KEY (topartner_id) REFERENCES public.partner(idpartner) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

\unrestrict hWaft0QgrlLH46W8JijekVFUIVndqcAw4pgtBF8MQd9BRJC7Ur7E6skK8T9lh5c

