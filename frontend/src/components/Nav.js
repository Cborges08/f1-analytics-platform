"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Nav() {
  const pathname = usePathname();

  const links = [
    { href: "/", label: "Dashboard" },
    { href: "/standings", label: "Standings" },
    { href: "/races", label: "Races" },
    { href: "/drivers", label: "Drivers" },
  ];

  return (
    <nav className="nav">
      <Link href="/" className="nav-logo">F1 Analytics</Link>
      <ul className="nav-links">
        {links.map(({ href, label }) => (
          <li key={href}>
            <Link href={href} className={pathname === href ? "active" : ""}>
              {label}
            </Link>
          </li>
        ))}
      </ul>
    </nav>
  );
}
