class ReportingPreference:
    for_recipient = 1
    for_transporter = 2
    for_suppiler = 3

    FieldStr = {
        for_recipient: "Original for Recipient",
        for_transporter: "Duplicate for Transporter",
        for_suppiler: "Triplicate for Supplier",
    }