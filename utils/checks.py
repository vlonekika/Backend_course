def is_number(text_data: str) -> bool:
     
     try: 
        float(text_data)
        return True 
     
     except:
          return False