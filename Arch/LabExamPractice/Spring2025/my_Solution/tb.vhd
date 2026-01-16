library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity TB is
end entity;

architecture arch_TB of TB is

  component washingMachineController is
    port (
      Clk      : in  std_logic;
      Reset    : in  std_logic; -- active low asynchronous reset
      en       : in  std_logic;
      fill_Led : out std_logic;
      wash_Led : out std_logic;
      rinse_Led: out std_logic;
      spin_Led : out std_logic
    );
  end component;

  constant clk_cycle : time := 50 ns;  -- use 50 ns for fast simulation

  signal Clk       : std_logic := '0';
  signal Reset     : std_logic := '1';
  signal en        : std_logic := '0';
  signal fill_Led  : std_logic := '0';
  signal wash_Led  : std_logic := '0';
  signal rinse_Led : std_logic := '0';
  signal spin_Led  : std_logic := '0';

begin

  -- Clock generator
  clk_simulation: process
  begin
    loop
      Clk <= '1';
      wait for clk_cycle / 2;
      Clk <= '0';
      wait for clk_cycle / 2;
    end loop;
  end process;

  -- Instantiate DUT
  DUT: washingMachineController
    port map (
      Clk       => Clk,
      Reset     => Reset,
      en        => en,
      fill_Led  => fill_Led,
      wash_Led  => wash_Led,
      rinse_Led => rinse_Led,
      spin_Led  => spin_Led
    );

  -- Self-checking test process
  mainProcess: process
    variable all_passed : boolean := true;
  begin
    Reset <= '1';
    wait until rising_edge(Clk);
    -- Reset pulse aligned to clock edges
    Reset <= '0';
    wait until rising_edge(Clk);
    Reset <= '1';
    wait until rising_edge(Clk);

    -- Enable controller
    en <= '1';

    -- ===== FILL state =====
    assert (fill_Led = '1' and wash_Led = '0' and rinse_Led = '0' and spin_Led = '0')
      report "FAIL: Expected FILL state right after reset" severity error;

    -- Wait for 60 cycles (3 s at 20 Hz)
      wait for 60*clk_cycle;

    assert (fill_Led = '0' and wash_Led = '1' and rinse_Led = '0' and spin_Led = '0')
      report "FAIL: Expected WASH state after 3 s" severity error;

    -- ===== WASH state =====
    wait for 100*clk_cycle;

    assert (fill_Led = '0' and wash_Led = '0' and rinse_Led = '1' and spin_Led = '0')
      report "FAIL: Expected RINSE state after additional 5 s" severity error;

    -- ===== RINSE state =====
    wait for 40 * clk_cycle;

    assert (fill_Led = '0' and wash_Led = '0' and rinse_Led = '0' and spin_Led = '1')
      report "FAIL: Expected SPIN state after additional 2 s" severity error;

    -- ===== SPIN state =====
    wait for 80 * clk_cycle;

    assert (fill_Led = '1' and wash_Led = '0' and rinse_Led = '0' and spin_Led = '0')
      report "FAIL: Expected FILL state after SPIN completed" severity error;

    report "TEST PASSED: washingMachineController passed all state-timing checks." severity note;

    wait; -- stop simulation
  end process mainProcess;

end architecture;
