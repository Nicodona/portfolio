import { useState } from "react";
import Reveal from "../components/Reveal.jsx";
import PageHeader from "../components/PageHeader.jsx";
import LinkOut from "../components/LinkOut.jsx";
import Socials from "../components/Socials.jsx";
import { sendContact } from "../api.js";
import { usePortfolio } from "../context/PortfolioContext.jsx";

export default function ContactPage() {
  const { data } = usePortfolio();
  const { profile } = data;
  const [form, setForm] = useState({ name: "", email: "", subject: "", message: "" });
  const [state, setState] = useState({ sending: false, note: null, ok: false });

  const update = (k) => (e) => setForm({ ...form, [k]: e.target.value });

  async function submit(e) {
    e.preventDefault();
    if (!form.name || !form.email || !form.message) {
      setState({
        sending: false,
        ok: false,
        note: "Please fill in your name, email and a message.",
      });
      return;
    }
    setState({ sending: true, note: null, ok: false });
    try {
      const res = await sendContact(form);
      setState({ sending: false, ok: true, note: res.detail });
      setForm({ name: "", email: "", subject: "", message: "" });
    } catch (err) {
      setState({
        sending: false,
        ok: false,
        note:
          err.status === 429
            ? "You are sending messages a little too fast. Give it a minute and try again."
            : "Something went wrong sending your message. You can always email me directly instead.",
      });
    }
  }

  return (
    <>
      <PageHeader
        eyebrow="Say hello"
        title="Get In Touch"
        lede="Whether you have a project in mind, a role you think I would fit,
        or you simply want to talk shop about data systems and school
        platforms, my inbox is always open."
      />

      <div className="contact-layout">
        <Reveal className="contact-wrap">
          <form className="contact-form" onSubmit={submit}>
            <div className="row">
              <input
                placeholder="Your name"
                value={form.name}
                onChange={update("name")}
                autoComplete="name"
              />
              <input
                placeholder="Your email"
                type="email"
                value={form.email}
                onChange={update("email")}
                autoComplete="email"
              />
            </div>
            <input
              placeholder="Subject (optional)"
              value={form.subject}
              onChange={update("subject")}
            />
            <textarea
              placeholder="What can I build for you?"
              value={form.message}
              onChange={update("message")}
            />
            <div>
              <button className="btn solid" type="submit" disabled={state.sending}>
                {state.sending ? "Sending..." : "Send message"}
              </button>
            </div>
            {state.note && (
              <div className={`form-note ${state.ok ? "ok" : "err"}`}>{state.note}</div>
            )}
          </form>
        </Reveal>

        <Reveal className="contact-aside">
          <div className="subhead">Direct lines</div>
          <ul className="contact-details">
            {profile.email && (
              <li>
                <span className="k">Email</span>
                <LinkOut href={`mailto:${profile.email}`}>{profile.email}</LinkOut>
              </li>
            )}
            {profile.whatsapp_number && (
              <li>
                <span className="k">WhatsApp</span>
                <LinkOut href={`https://wa.me/${profile.whatsapp_number}`}>
                  Chat on WhatsApp
                </LinkOut>
              </li>
            )}
            {profile.phone && (
              <li>
                <span className="k">Phone</span>
                <span>{profile.phone}</span>
              </li>
            )}
            {profile.location && (
              <li>
                <span className="k">Based in</span>
                <span>
                  {profile.location} · {profile.timezone_label}
                </span>
              </li>
            )}
          </ul>
          <Socials profile={profile} />
        </Reveal>
      </div>
    </>
  );
}
