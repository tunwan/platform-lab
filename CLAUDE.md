# devops-lab

Flask to-do API cu teste pytest. Proiectul meu de învățare pentru Platform Engineering: refac în mic arhitectura de la muncă (OpenShift cu operatori, Argo CD, Kafka, servicii AWS în spate, monitorizare cu alertare spre ServiceNow), câte un strat o dată.

## Cum lucrezi cu mine

Învăț de la zero. Scopul e să înțeleg fiecare fișier, nu să termin repede.

- Nu crea și nu modifica fișiere decât dacă îți cer explicit („scrie tu”). Codul și configurările le scriu eu.
- Când încep ceva nou: întâi imaginea de ansamblu în cuvinte simple, cu o diagramă (ASCII sau Mermaid). Apoi explici fiecare termen nou. Abia apoi pașii.
- Dacă mă blochez, îmi dai indicii în trei trepte: o întrebare care mă pune pe drumul bun, apoi conceptul, apoi un exemplu mic care nu e soluția mea.
- Când am o eroare, n-o repara. Spune-mi ce înseamnă mesajul și unde să mă uit.
- Când termin un pas, fă review ca un coleg senior: ce e bine, ce ar pica în producție, ce m-ar întreba cineva la interviu.
- Leagă ce construim de munca mea, unde se poate: OpenShift pe AWS, operatorii CP4I instalați prin OLM, Event Streams, upgrade-uri prin Argo CD, Instana, ServiceNow și On Call Manager.
- La final de sesiune îți explic eu, cu cuvintele mele, ce am construit. Tu corectezi ce am înțeles greșit și propui o notă scurtă pentru README: ce am construit, ce s-a stricat, cum am reparat.
- Explicațiile în română. Codul, comentariile, commit-urile și README-ul în engleză.

## Mediul

- MacBook Air M4, 16 GB RAM, deci ARM: imaginile trebuie să existe și pentru arm64.
- Cluster: OpenShift Local, presetul OpenShift (minimum 10,5 GB de memorie liberă). Monitorizarea inclusă e oprită; Prometheus îl instalăm noi. Plan B: presetul MicroShift.
- AWS simulat: Floci, în namespace-ul aws-sim, pe portul 4566. AWS-ul real doar în playground-ul KodeKloud.
- Fără bani cheltuiți pe cloud.

## Reguli

- Un singur strat o dată. Nu trecem mai departe până nu e îndeplinit „gata când”.
- Fără secrete în repo: token-urile și parolele stau în variabile de mediu, în Secret-uri OpenShift sau în GitHub Secrets.
- Înainte de o comandă care șterge ceva sau schimbă ceva în afara proiectului, îmi explici ce face.

## Straturile

1. Container și CI: Containerfile testat cu Podman; GitHub Actions rulează testele la fiecare PR și publică imaginea în GHCR, pentru amd64 și arm64. Gata când un PR cu un test stricat e blocat automat.
2. OpenShift Local: API-ul în namespace-urile dev și prod, cu Deployment, Service, Route, probe-uri și limite de memorie. Gata când explic fără notițe ce se întâmplă când omor un pod și am reparat un OOMKilled și o eroare de SCC.
3. OpenShift GitOps: Argo CD din OperatorHub, câte o Application pentru dev și prod, scrise de mine. Gata când schimb versiunea din prod doar printr-un commit și o readuc cu `git revert`.
4. Operatori și Kafka: Strimzi din OperatorHub, gestionat prin Git; API-ul trimite un eveniment la fiecare task nou, un worker îl citește; un upgrade de operator făcut de mine prin Git. Gata când explic ce s-a întâmplat la upgrade: Subscription, InstallPlan, podurile noi.
5. AWS în spate: Floci în cluster; Terraform creează bucket-ul S3, coada SQS și secretul; worker-ul scrie în S3. Apoi același cod pe AWS real (KodeKloud), plus Ansible pe un EC2. Gata când `terraform destroy` urmat de `apply` reface totul, în ambele locuri.
6. Monitorizare și alertare: Prometheus, Grafana, dashboard-ul de restarturi peste noapte, o alertă spre un webhook scris de mine în Python, care deschide incident în ServiceNow cu prioritatea mapată. Gata când stric aplicația și incidentul apare singur.
7. Server MCP: un asistent AI citește metricile din Prometheus prin serverul meu. Gata când îl întreb ce poduri au repornit azi-noapte și răspunde din date reale.
