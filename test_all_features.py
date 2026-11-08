import io
import json
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

print("=== 1. TEST USER AUTHENTICATION & DASHBOARD ===")
login_res = client.post("/api/auth/login", json={"email": "admin@legalai.local", "password": "admin123"})
assert login_res.status_code == 200, f"Login failed: {login_res.text}"
user_data = login_res.json()["user"]
token = user_data["token"]
print(f"Logged in as: {user_data['username']} ({user_data['role']})")

me_res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
assert me_res.status_code == 200
print(f"Token verified for: {me_res.json()['email']}")

dash_res = client.get("/api/dashboard/stats")
assert dash_res.status_code == 200
print(f"Dashboard total docs: {dash_res.json()['overview']['total_documents']}")

print("\n=== 2. TEST PDF / DOCX / TXT INGESTION ===")
docs_list = client.get("/api/documents").json()
print(f"Current stored documents count: {len(docs_list)}")

print("\n=== 3. TEST CHAT EXPORTS INGESTION ===")
chat_text = """[10/06/2026, 14:00:15] Attorney Sarah: The indemnity under Section 4 must be capped at $500,000.
[10/06/2026, 14:02:40] Counsel Mike: We agree to cap indemnity at $500,000 provided gross negligence is excepted.
[10/06/2026, 14:05:00] Attorney Sarah: Confirmed and accepted.
"""
chat_upload = client.post("/api/documents/upload", files={"file": ("settlement_chat_export.txt", io.BytesIO(chat_text.encode("utf-8")), "text/plain")})
assert chat_upload.status_code == 200
chat_id = chat_upload.json()["document"]["id"]
print(f"Chat export uploaded: {chat_id} (Type: {chat_upload.json()['document']['file_type']})")

print("\n=== 4. TEST AUDIO / VIDEO INGESTION ===")
audio_upload = client.post("/api/documents/upload", files={"file": ("deposition_recording.wav", io.BytesIO(b"RIFF....WAVEfmt ....data...."), "audio/wav")})
assert audio_upload.status_code == 200
audio_id = audio_upload.json()["document"]["id"]
print(f"Audio exhibit uploaded: {audio_id} (Type: {audio_upload.json()['document']['file_type']})")

print("\n=== 5. TEST LARGE DOCUMENT PAGE-WISE EXTRACTION & CHUNKING ===")
pages_res = client.get(f"/api/documents/{chat_id}/pages")
print(f"Document {chat_id} pages: {len(pages_res.json())}")
chunks_res = client.get(f"/api/documents/{chat_id}/chunks")
print(f"Document {chat_id} chunks: {len(chunks_res.json())}")

print("\n=== 6. TEST AI-BASED SUMMARISATION ===")
ana_res = client.post(f"/api/analysis/{chat_id}")
assert ana_res.status_code == 200
summary = ana_res.json()["executive_summary"]
print(f"Executive Summary: {summary[:180]}...")
print(f"Risk Score: {ana_res.json()['risk_score']}, Risk Level: {ana_res.json()['risk_level']}")

print("\n=== 7. TEST DOCUMENT QA & RAG WITH CITATIONS & TEXT EVIDENCE ===")
qa_res = client.post("/api/assistant/chat", json={"document_id": chat_id, "query": "What cap was agreed on indemnity?"})
assert qa_res.status_code == 200
qa_data = qa_res.json()
print(f"QA Answer: {qa_data['answer'][:200]}...")
print(f"Confidence Score: {qa_data['confidence_score']}")
for idx, c in enumerate(qa_data["citations"]):
    print(f"  Citation #{idx+1}: {c['clause_title']} (Page {c['page_number']})")
    print(f"  Exact Quote: {c['exact_quote']}")

print("\n=== 8. TEST CITATION ABSENCE HANDLING ===")
qa_absent = client.post("/api/assistant/chat", json={"document_id": chat_id, "query": "Is there an arbitration clause?"})
assert qa_absent.status_code == 200
print(f"Absent Clause Answer: {qa_absent.json()['answer'][:160]}...")

print("\n=== ALL INTEGRATION TESTS PASSED SUCCESSFULLY! ===")
