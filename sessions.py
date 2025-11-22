import uuid
import time

class SessionManager:
    def __init__(self):
        self.sessions = {}
        self.expiration_time = 86400
    def create_session(self):
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "data": {},
            "created": time.time()
        }
        
        return session_id
    
    
    def get(self, id):
        session = self.sessions.get(id)
        if not session:
            return None
        
        if time.time() - session["created"] > self.expiration_time:
            del self.sessions[id]
            return None
            
        return session
    
    
    def save(self, id, data):
        if id in self.sessions:
            self.sessions[id]["data"] = data