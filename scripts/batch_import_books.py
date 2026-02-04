#!/usr/bin/env python3
"""Batch import script for docs/books/ into knowledge base.

This script categorizes and imports all books from the docs/books directory
into the appropriate agent domains.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from knowledge.importer import KnowledgeImporter, AgentDomain

# Book categorization mapping
# Format: (filename_pattern, agent_domain, tags, title_override)
BOOK_MAPPINGS = [
    # ============ AZURE / MICROSOFT ============
    # Azure Architecture
    ("examrefaz-304", "azure-architecture", ["certification", "az-304", "architect"], "AZ-304 Architect Design"),
    ("examrefaz-305", "azure-architecture", ["certification", "az-305", "infrastructure"], "AZ-305 Infrastructure Solutions"),
    ("azurecloudnativearchitecturemapbook", "azure-architecture", ["cloud-native", "architecture"], "Azure Cloud Native Architecture"),
    ("azurecloudprojects", "azure-architecture", ["projects", "hands-on"], "Azure Cloud Projects"),
    ("azuredevopsexplained", "azure-architecture", ["devops", "cicd"], "Azure DevOps Explained"),
    ("azurefordevelopers", "azure-architecture", ["development", "sdk"], "Azure for Developers"),

    # Azure Networking
    ("examrefaz-700", "azure-networking", ["certification", "az-700", "networking"], "AZ-700 Azure Networking"),
    ("azurenetworkingcookbook", "azure-networking", ["recipes", "practical"], "Azure Networking Cookbook"),

    # Azure Security
    ("examrefaz-500", "azure-security", ["certification", "az-500", "security"], "AZ-500 Azure Security"),
    ("examrefsc-100", "azure-security", ["certification", "sc-100", "cybersecurity-architect"], "SC-100 Cybersecurity Architect"),
    ("examrefsc-200", "azure-security", ["certification", "sc-200", "security-operations"], "SC-200 Security Operations"),
    ("examrefsc-300", "azure-security", ["certification", "sc-300", "identity"], "SC-300 Identity & Access"),
    ("examrefsc-900", "azure-security", ["certification", "sc-900", "fundamentals"], "SC-900 Security Fundamentals"),

    # Azure General Certifications (azure-architecture as default)
    ("examrefaz-104", "azure-architecture", ["certification", "az-104", "administrator"], "AZ-104 Azure Administrator"),
    ("examrefaz-204", "azure-architecture", ["certification", "az-204", "developer"], "AZ-204 Azure Developer"),
    ("examrefaz-800", "azure-architecture", ["certification", "az-800", "hybrid"], "AZ-800 Hybrid Core Infrastructure"),
    ("examrefaz-801", "azure-architecture", ["certification", "az-801", "hybrid-advanced"], "AZ-801 Hybrid Advanced Services"),
    ("examrefaz-900", "azure-architecture", ["certification", "az-900", "fundamentals"], "AZ-900 Azure Fundamentals"),
    ("examrefdp-500", "azure-architecture", ["certification", "dp-500", "analytics"], "DP-500 Enterprise Analytics"),
    ("examrefdp-600", "azure-architecture", ["certification", "dp-600", "fabric"], "DP-600 Microsoft Fabric"),
    ("examrefdp-900", "azure-architecture", ["certification", "dp-900", "data-fundamentals"], "DP-900 Data Fundamentals"),
    ("examrefms-102", "azure-architecture", ["certification", "ms-102", "365-admin"], "MS-102 Microsoft 365 Administrator"),
    ("examrefms-500", "azure-architecture", ["certification", "ms-500", "365-security"], "MS-500 Microsoft 365 Security"),
    ("examrefms-700", "azure-architecture", ["certification", "ms-700", "teams"], "MS-700 Microsoft Teams"),
    ("examrefms-900", "azure-architecture", ["certification", "ms-900", "365-fundamentals"], "MS-900 Microsoft 365 Fundamentals"),
    ("examrefpl-300", "azure-architecture", ["certification", "pl-300", "power-bi"], "PL-300 Power BI"),
    ("examrefpl-900", "azure-architecture", ["certification", "pl-900", "power-platform"], "PL-900 Power Platform Fundamentals"),
    ("examrefai-900", "azure-architecture", ["certification", "ai-900", "ai-fundamentals"], "AI-900 Azure AI Fundamentals"),
    ("masteringendpointmanagement", "azure-architecture", ["intune", "endpoint", "management"], "Mastering Endpoint Management"),

    # ============ KUBERNETES ============
    ("bookofkubernetes", "kubernetes", ["fundamentals", "practical"], "The Book of Kubernetes"),
    ("certifiedkubernetessecurityspecialist", "kubernetes", ["certification", "cks", "security"], "CKS Study Guide"),
    ("cloudnativewithkubernetes", "kubernetes", ["cloud-native", "patterns"], "Cloud Native with Kubernetes"),
    ("deploycontainerapplicationsusingkubernetes", "kubernetes", ["containers", "deployment"], "Deploy Container Applications"),
    ("hands-onmicroserviceswithkubernetes", "kubernetes", ["microservices", "hands-on"], "Hands-On Microservices with K8s"),
    ("kubernetesrecipes", "kubernetes", ["recipes", "practical"], "Kubernetes Recipes"),
    ("kubernetesforgenerativeai", "kubernetes", ["ai", "ml", "gpu"], "Kubernetes for Generative AI"),

    # ============ SECURITY / OFFENSIVE ============
    ("advancedpenetrationtesting", "security-offensive", ["pentest", "advanced"], "Advanced Penetration Testing"),
    ("adversarialtradecraft", "security-offensive", ["adversary", "tradecraft"], "Adversarial Tradecraft"),
    ("appliedincidentresponse", "security-offensive", ["incident-response", "ir"], "Applied Incident Response"),
    ("attacksurfacemanagement", "security-offensive", ["asm", "attack-surface"], "Attack Surface Management"),
    ("artofdeception", "security-offensive", ["social-engineering", "deception"], "Art of Deception"),
    ("artofintrusion", "security-offensive", ["intrusion", "hacking-stories"], "Art of Intrusion"),
    ("artofmemoryforensics", "security-offensive", ["memory-forensics", "malware"], "Art of Memory Forensics"),
    ("certifiedinformationsecuritymanager", "security-offensive", ["cism", "certification"], "CISM Exam Prep"),
    ("cybersecurityblueteamtoolkit", "security-offensive", ["blue-team", "defense"], "Cybersecurity Blue Team Toolkit"),
    ("huntingcybercriminals", "security-offensive", ["osint", "threat-hunting"], "Hunting Cyber Criminals"),
    ("howirobbanks", "security-offensive", ["social-engineering", "physical"], "How I Rob Banks"),
    ("identity-nativeinfrastructure", "security-offensive", ["identity", "iam", "zero-trust"], "Identity-Native Infrastructure"),
    ("intelligentcontinuoussecurity", "security-offensive", ["devsecops", "continuous-security"], "Intelligent Continuous Security"),
    ("investigatingcryptocurrencies", "security-offensive", ["crypto", "blockchain-forensics"], "Investigating Cryptocurrencies"),
    ("languageofdeception", "security-offensive", ["ai-security", "deception"], "Language of Deception"),
    ("malwareanalystscookbook", "security-offensive", ["malware-analysis", "reverse-engineering"], "Malware Analyst's Cookbook"),
    ("securityengineering", "security-offensive", ["security-engineering", "design"], "Security Engineering"),
    ("tamingthehackingstorm", "security-offensive", ["defense", "framework"], "Taming the Hacking Storm"),
    ("tribeofhackers", "security-offensive", ["interviews", "career"], "Tribe of Hackers"),
    ("unauthorised_access", "security-offensive", ["physical-pentest", "social-engineering"], "Unauthorised Access"),
    ("webapplicationhackershandbook", "security-offensive", ["web-security", "owasp"], "Web Application Hacker's Handbook"),
    ("webapplicationsecurity", "security-offensive", ["web-security", "appsec"], "Web Application Security"),
    ("wiresharkforsecurityprofessionals", "security-offensive", ["wireshark", "network-analysis"], "Wireshark for Security Pros"),

    # ============ PROGRAMMING ============
    ("50algorithmseveryprogrammer", "programming", ["algorithms", "fundamentals"], "50 Algorithms Every Programmer Should Know"),
    ("cdatastructuresandalgorithms", "programming", ["c", "data-structures", "algorithms"], "C Data Structures and Algorithms"),

    # ============ PYTHON ============
    ("expertpythonprogramming", "python-engineering", ["advanced", "best-practices"], "Expert Python Programming"),
    ("buildingaiintensivepythonapplications", "python-engineering", ["ai", "applications"], "Building AI-Intensive Python Apps"),
    ("datascienceessentialsinpython", "python-engineering", ["data-science", "essentials"], "Data Science Essentials in Python"),

    # ============ JAVASCRIPT / TYPESCRIPT ============
    ("javascriptfrombeginner", "javascript-engineering", ["fundamentals", "beginner"], "JavaScript from Beginner to Pro"),
    ("full-stackwebdevelopmentwithtypescript", "javascript-engineering", ["typescript", "fullstack"], "Full-Stack TypeScript Development"),
    ("hands-onmicroserviceswithjavascript", "javascript-engineering", ["microservices", "nodejs"], "Hands-On Microservices with JS"),

    # ============ GO ============
    ("goprogramming", "go-engineering", ["fundamentals", "beginner-to-pro"], "Go Programming"),

    # ============ RUBY ============
    ("polishedrubyprogramming", "ruby-engineering", ["advanced", "best-practices"], "Polished Ruby Programming"),

    # ============ C++ ============
    ("cplusplushighperformance", "cpp-engineering", ["performance", "optimization"], "C++ High Performance"),

    # ============ DATA SCIENCE / AI / ML ============
    ("aiagentsandapplications", "data-science", ["ai-agents", "applications"], "AI Agents and Applications"),
    ("aiapplicationsmadeeasy", "data-science", ["ai", "practical"], "AI Applications Made Easy"),
    ("ai-assistedcoding", "data-science", ["ai-coding", "copilot"], "AI-Assisted Coding"),
    ("aiandmlpoweringtheagents", "data-science", ["ai", "ml", "automation"], "AI and ML Powering Automation"),
    ("aiproductmanagershandbook", "data-science", ["ai", "product-management"], "AI Product Manager's Handbook"),
    ("apracticalapproachformachinelearning", "data-science", ["ml", "deep-learning", "practical"], "Practical ML and Deep Learning"),
    ("buildingmachinelearningpoweredapplications", "data-science", ["ml", "applications"], "Building ML-Powered Applications"),
    ("datasciencefromscratch", "data-science", ["fundamentals", "from-scratch"], "Data Science from Scratch"),
    ("datascience_thehardparts", "data-science", ["advanced", "challenges"], "Data Science: The Hard Parts"),
    ("datascienceatthecommandline", "data-science", ["cli", "unix"], "Data Science at the Command Line"),
    ("generativeaiforsoftwaredevelopers", "data-science", ["generative-ai", "llm"], "Generative AI for Developers"),
    ("hands-ongraphneuralnetworks", "data-science", ["gnn", "deep-learning"], "Hands-On Graph Neural Networks"),
    ("algorithmiclearninginarandomworld", "data-science", ["ml-theory", "algorithms"], "Algorithmic Learning in a Random World"),

    # ============ LINUX / DEVOPS ============
    ("bashidioms", "linux-administration", ["bash", "shell", "idioms"], "Bash Idioms"),
    ("comptialinuxpluscertificationcompanion", "linux-administration", ["certification", "linux+"], "CompTIA Linux+ Certification"),
    ("enterpriselinuxadministrator", "linux-administration", ["enterprise", "career"], "Enterprise Linux Administrator"),
    ("linuxcontainersandvirtualization", "linux-administration", ["containers", "virtualization"], "Linux Containers & Virtualization"),
    ("probash", "linux-administration", ["bash", "advanced"], "Pro Bash Programming"),

    # ============ SOFTWARE ARCHITECTURE ============
    ("buildingmicroservices2e", "software-architecture", ["microservices", "patterns"], "Building Microservices 2e"),
    ("buildingmulti-tenantsaas", "software-architecture", ["saas", "multi-tenant"], "Building Multi-Tenant SaaS"),
    ("buildingevent-drivenmicroservices", "software-architecture", ["event-driven", "microservices"], "Building Event-Driven Microservices"),
    ("ciandcddesignpatterns", "software-architecture", ["cicd", "patterns"], "CI/CD Design Patterns"),
    ("cloudapplicationarchitecturepatterns", "software-architecture", ["cloud", "patterns"], "Cloud Application Architecture Patterns"),
    ("communicationpatterns", "software-architecture", ["communication", "integration"], "Communication Patterns"),
    ("flowarchitectures", "software-architecture", ["flow", "streaming"], "Flow Architectures"),
    ("foundationsofscalablesystems", "software-architecture", ["scalability", "fundamentals"], "Foundations of Scalable Systems"),
    ("fundamentalsofsoftwarearchitecture", "software-architecture", ["fundamentals", "patterns"], "Fundamentals of Software Architecture"),
    ("grpc_upandrunning", "software-architecture", ["grpc", "api"], "gRPC Up and Running"),
    ("learningsystemsthinking", "software-architecture", ["systems-thinking", "design"], "Learning Systems Thinking"),
    ("solutionsarchitectshandbook", "software-architecture", ["solutions-architect", "handbook"], "Solutions Architect's Handbook"),
    ("solutionsarchitectsinterview", "software-architecture", ["interview", "career"], "Solutions Architect's Interview"),

    # ============ CLOUD ARCHITECTURE ============
    ("architectinggooglecloudsolutions", "cloud-architecture", ["gcp", "architecture"], "Architecting Google Cloud Solutions"),
    ("awscertifiedsolutionsarchitect", "cloud-architecture", ["aws", "certification", "solutions-architect"], "AWS Solutions Architect"),
    ("oraclecloudinfrastructure", "cloud-architecture", ["oci", "oracle"], "Oracle Cloud Infrastructure"),
    ("professionalcloudarchitect", "cloud-architecture", ["gcp", "certification"], "GCP Professional Cloud Architect"),
    ("cloudsolutionarchitectscareer", "cloud-architecture", ["career", "cloud"], "Cloud Solution Architect Career"),
    ("getting-started-with-crossplane", "cloud-architecture", ["crossplane", "iac"], "Getting Started with Crossplane"),

    # ============ CRYPTOGRAPHY ============
    ("applied_cryptography", "cryptography", ["algorithms", "protocols"], "Applied Cryptography"),
    ("cryptographyengineering", "cryptography", ["engineering", "practical"], "Cryptography Engineering"),

    # ============ iOS ============
    ("aniosdevelopersguidetoswiftui", "ios-engineering", ["swiftui", "ios"], "iOS Developer's Guide to SwiftUI"),

    # ============ REVERSE ENGINEERING ============
    ("practical_reverse_engineering", "reverse-engineering", ["x86", "arm", "windows"], "Practical Reverse Engineering"),
    ("x86softwarereverse-engineering", "reverse-engineering", ["x86", "cracking"], "x86 Software Reverse Engineering"),
    ("foundationsofarm64linuxdebugging", "reverse-engineering", ["arm64", "debugging", "linux"], "ARM64 Linux Debugging"),
    ("foundationsoflinuxdebugging", "reverse-engineering", ["x86", "debugging", "linux"], "Linux Debugging Foundations"),
    ("threat_modeling", "reverse-engineering", ["threat-modeling", "security-design"], "Threat Modeling"),

    # ============ DATA ENGINEERING ============
    ("buildingananonymizationpipeline", "data-engineering", ["anonymization", "privacy"], "Building Anonymization Pipeline"),
    ("enterprisedatacatalog", "data-engineering", ["data-catalog", "governance"], "Enterprise Data Catalog"),
    ("practicallakehousearchitecture", "data-engineering", ["lakehouse", "architecture"], "Practical Lakehouse Architecture"),
]


def normalize_filename(filename: str) -> str:
    """Normalize filename for matching by removing special chars and lowercasing."""
    return filename.lower().replace("-", "").replace("_", "").replace(" ", "").replace("(", "").replace(")", "")


def find_matching_mapping(filename: str):
    """Find the matching mapping for a given filename."""
    normalized = normalize_filename(filename)
    for pattern, domain, tags, title in BOOK_MAPPINGS:
        if pattern.replace("-", "").replace("_", "") in normalized:
            return (domain, tags, title)
    return None


def main():
    books_dir = project_root / "docs" / "books"
    if not books_dir.exists():
        print(f"Error: Books directory not found: {books_dir}")
        sys.exit(1)

    importer = KnowledgeImporter()

    # Get all supported files
    supported_extensions = {".epub", ".pdf", ".txt", ".md", ".mp4", ".mkv", ".webm", ".wav", ".mp3"}
    files = [f for f in books_dir.iterdir() if f.is_file() and f.suffix.lower() in supported_extensions]

    print(f"Found {len(files)} files to process")
    print("=" * 60)

    imported = 0
    skipped = 0
    errors = []

    for filepath in sorted(files):
        mapping = find_matching_mapping(filepath.name)

        if not mapping:
            print(f"SKIP (no mapping): {filepath.name}")
            skipped += 1
            continue

        domain, tags, title = mapping

        print(f"\nImporting: {filepath.name}")
        print(f"  -> Domain: {domain}")
        print(f"  -> Tags: {tags}")
        print(f"  -> Title: {title}")

        try:
            metadata = importer.import_file(
                filepath,
                agent=domain,
                tags=tags,
                title=title,
                chunk_size=200000,
                chunk_overlap=1000,
            )
            print(f"  -> Success! ID: {metadata.id}")
            print(f"  -> Chunks: {metadata.chunk_count}, Chars: {metadata.char_count}")
            if metadata.duration_seconds:
                mins = int(metadata.duration_seconds // 60)
                secs = int(metadata.duration_seconds % 60)
                print(f"  -> Duration: {mins}m {secs}s")
            imported += 1
        except Exception as e:
            print(f"  -> ERROR: {e}")
            errors.append((filepath.name, str(e)))

    print("\n" + "=" * 60)
    print(f"SUMMARY")
    print(f"  Imported: {imported}")
    print(f"  Skipped (no mapping): {skipped}")
    print(f"  Errors: {len(errors)}")

    if errors:
        print("\nERRORS:")
        for name, err in errors:
            print(f"  - {name}: {err}")


if __name__ == "__main__":
    main()
