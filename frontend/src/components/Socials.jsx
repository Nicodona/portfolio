import { GitHubIcon, LinkedInIcon, MailIcon, WhatsAppIcon } from "./Icons.jsx";

export default function Socials({ profile }) {
  return (
    <div className="socials">
      {profile.github_url && (
        <a href={profile.github_url} target="_blank" rel="noreferrer" title="GitHub">
          <GitHubIcon />
        </a>
      )}
      {profile.linkedin_url && (
        <a href={profile.linkedin_url} target="_blank" rel="noreferrer" title="LinkedIn">
          <LinkedInIcon />
        </a>
      )}
      {profile.email && (
        <a href={`mailto:${profile.email}`} title="Email">
          <MailIcon />
        </a>
      )}
      {profile.whatsapp_number && (
        <a
          href={`https://wa.me/${profile.whatsapp_number}`}
          target="_blank"
          rel="noreferrer"
          title="WhatsApp"
        >
          <WhatsAppIcon />
        </a>
      )}
    </div>
  );
}
