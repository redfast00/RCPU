.data
    ;
    ; syscalls
    ;
    .sys_printf 0
    .sys_fgets 1
    .sys_getc 2
    .stdin 0
    .format_str string '%s'
    .placeholder string '0'

    ;
    ; brainfuck structures
    ;
    .tape allocate 256
    .tapesize 256
    .max_cell_value 255
    .program allocate 1024
    .programsize 1024

    ; pointer to lenght of program tape
    .p_program_len allocate 1

    ; pointer to address of current location on program tape
    .p_program_current_loc allocate 1

    ; pointer to address of current location on data tape
    .p_tape_current_loc allocate 1

    ;
    ; Characters
    ;
    .char_fill_tape 0
    .char_nul 0

    .char_plus 43
    .char_minus 45
    .char_inc_tape_ptr 62
    .char_dec_tape_ptr 60
    .char_print 46
    .char_input 44
    .char_forward_cond_jump 91
    .char_backward_cond_jump 93
    
    ;
    ; Strings
    ;
    .done_parsing string "Done parsing\n"

.text
.global main:
    main:
        LDV D, initialize:
        CAL D
        LDV D, clear_tape:
        CAL D
        LDV D, input_program:
        CAL D
        LDV D, .done_parsing
        PSH D
        LDV D, .sys_printf
        PSH D
        SYS
        
        while_true_do_mainloop:
            LDV D, mainloop:
            CAL D
            JMP while_true_do_mainloop:

    initialize:
        ; This should be LDV16, but was manually optimized to LDV
        LDV C, .p_program_current_loc
        LDV A, .p_tape_current_loc
        LDV16 D, .program
        LDP C, D
        LDV16 D, .tape
        LDP A, D
        RET

    clear_tape:
        LDV A, .tapesize
        LDV16 D, .tape
        loop_clear_tape:
            LDV B, .char_fill_tape
            LDP D, B
            INC D
            DEC A
            ; check if we need to end the loop
            LDV B, 1
            LDV C, end_loop_clear_tape:
            JLT B, C
            JMP loop_clear_tape:
        end_loop_clear_tape:
        RET

    input_program:
        LDV D, .stdin
        PSH D
        LDV16 D, .programsize
        PSH D
        LDV16 D, .program
        PSH D
        LDV D, .sys_fgets
        PSH D
        SYS
        LDV16 C, .p_program_len
        POP D
        LDP C, D
        RET

    fetch:
        ; fetches the current character and places it in the A register
        ; load pointer to pointer to current character
        LDV A, .p_program_current_loc
        ; load pointer to cur char into A
        LDR A, A
        ; load cur char into A
        LDR A, A
        RET

    mainloop:
        LDV C, fetch:
        CAL C
        ;
        ; compare character to instructions
        ;

        ; Push return address onto the stack so RET will work in BF instruction calls
        LDV C, return_into_mainloop:
        PSH C

        ; Check if current char is nul (end of program)
        LDV C, .char_nul
        LDV D, endprogram:
        JEQ C, D

        ; Check if current char is '+' (increment current cell)
        LDV C, .char_plus
        LDV D, plus:
        JEQ C, D

        ; Check if current char is '-' (decrement current cell)
        LDV C, .char_minus
        LDV D, minus:
        JEQ C, D

        ; Check if current char is '>' (increment cell pointer)
        LDV C, .char_inc_tape_ptr
        LDV D, inc_tape_ptr:
        JEQ C, D

        ; Check if current char is '<' (decrement cell pointer)
        LDV C, .char_dec_tape_ptr
        LDV D, dec_tape_ptr:
        JEQ C, D

        ; Check if current char is '.' (print current cell)
        LDV C, .char_print
        LDV D, print:
        JEQ C, D

        ; Check if current char is ',' (input char into current cell)
        LDV C, .char_input
        LDV D, input_char:
        JEQ C, D

        ; Check if current char is '[' (forward jump to matching ] if current cell is 0)
        LDV C, .char_forward_cond_jump
        LDV D, forward_cond_jump:
        JEQ C, D

        ; Check if current char is ']' (backward jump to matching [ if current cell is not 0)
        LDV C, .char_backward_cond_jump
        LDV D, backward_cond_jump:
        JEQ C, D

        return_into_mainloop:
        RET

    next_instruction:
        LDV A, .p_program_current_loc
        LDR B, A
        INC B
        LDP A, B
        RET

    endprogram:
        ; Sentinel values
        LDV A, 123
        LDV B, 456
        LDV C, 789
        LDV D, .p_tape_current_loc
        LDR D,D
        LDR D,D
        HLT

    plus:
        LDV A, .p_tape_current_loc
        ; address of current cell in A
        LDR A, A
        ; value of current cell in B
        LDR B, A
        INC B
        LDV C, .max_cell_value
        AND B, C
        ; store value in program tape
        LDP A, B
        LDV A, next_instruction:
        CAL A
        RET

    minus:
        LDV A, .p_tape_current_loc
        ; address of current cell in A
        LDR A, A
        ; value of current cell in B
        LDR B, A
        DEC B
        LDV C, .max_cell_value
        AND B, C
        ; store value in program tape
        LDP A, B
        LDV A, next_instruction:
        CAL A
        RET

    print:
        LDV A, .p_tape_current_loc
        ; address of current cell in A
        LDR A, A
        ; value of current cell in B
        LDR A, A
        LDV16 B, .placeholder
        LDP B, A
        PSH B
        LDV16 A, .format_str
        PSH A
        LDV A, .sys_printf
        PSH A
        SYS
        LDV A, next_instruction:
        CAL A
        RET

    inc_tape_ptr:
        LDV A, .p_tape_current_loc
        ; address of current cell in B
        LDR B, A
        INC B
        LDP A, B
        LDV A, next_instruction:
        CAL A
        RET

    dec_tape_ptr:
        LDV A, .p_tape_current_loc
        ; address of current cell in B
        LDR B, A
        DEC B
        LDP A, B
        LDV A, next_instruction:
        CAL A
        RET

    input_char:
        LDV A, .stdin
        PSH A
        LDV A, .sys_getc
        PSH A
        SYS
        POP B
        ; character that was read is in D
        LDV A, .p_tape_current_loc
        ; address of current cell in A
        LDR A, A
        LDP A, B
        LDV A, next_instruction:
        CAL A
        RET

    forward_cond_jump:
        LDV A, .p_tape_current_loc
        LDR A, A
        ; value of current cell in A
        LDR A, A
        LDV B, 0
        LDV C, do_forward_jmp:
        JEQ B, C
            LDV A, next_instruction:
            CAL A
            RET
        do_forward_jmp:
            ; Push matched characters
            LDV A, 0
            PSH A
            LDV B, .p_program_current_loc
            ; load pointer to cur char into B
            LDR B, B
            loop_do_forward_jump:
                ; load cur char into A
                LDR A, B
                LDV C, .char_forward_cond_jump
                LDV D, forward_match_forward_cond_jump:
                JEQ C, D

                LDV C, .char_backward_cond_jump
                LDV D, backward_match_forward_cond_jump:
                JEQ C, D
                ; None of the characters matched
                INC B
                JMP loop_do_forward_jump:
            check_forward_loop_done:
                POP A
                LDV D, forward_loop_done:
                LDV C, 0
                JEQ C, D
                PSH A
                JMP loop_do_forward_jump:
            forward_loop_done:
                LDV D, .p_program_current_loc
                LDP D, B
                RET
    forward_match_forward_cond_jump:
        POP C
        INC C
        PSH C
        INC B
        JMP check_forward_loop_done:

    backward_match_forward_cond_jump:
        POP C
        DEC C
        PSH C
        INC B
        JMP check_forward_loop_done:

    backward_cond_jump:
        LDV B, .p_tape_current_loc
        LDR B, B
        ; value of current cell in B
        LDR B, B
        LDV A, 0
        LDV C, do_backward_jmp:
        JNE B, C
            LDV A, next_instruction:
            CAL A
            RET
        do_backward_jmp:
            ; Push matched characters
            LDV A, 0
            PSH A
            LDV B, .p_program_current_loc
            ; load pointer to cur char into B
            LDR B, B
            loop_do_backward_jump:
                ; load cur char into A
                LDR A, B
                LDV C, .char_forward_cond_jump
                LDV D, forward_match_backward_cond_jump:
                JEQ C, D
                LDV C, .char_backward_cond_jump
                LDV D, backward_match_backward_cond_jump:
                JEQ C, D
                ; None of the characters matched
                DEC B
                JMP loop_do_backward_jump:
            check_backward_loop_done:
                POP A
                LDV D, backward_loop_done:
                LDV C, 0
                JEQ C, D
                PSH A
                JMP loop_do_backward_jump:
            backward_loop_done:
                LDV D, .p_program_current_loc
                INC B
                ;INC B
                LDP D, B
                RET
    forward_match_backward_cond_jump:
        POP C
        INC C
        PSH C
        DEC B
        JMP check_backward_loop_done:

    backward_match_backward_cond_jump:
        POP C
        DEC C
        PSH C
        DEC B
        JMP check_backward_loop_done:
