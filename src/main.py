from frontend.interface import ConciliacionBancaria
from backend.reconciliation import Reconciliation
from backend.reconciliation_report import ReconciliationReport

def main():
    """Inicia la aplicación de conciliación bancaria"""
    app = ConciliacionBancaria()
    app.mainloop()

if __name__ == "__main__":
    main()
